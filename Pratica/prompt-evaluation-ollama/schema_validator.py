"""
Mariana-Prompt: Schema enforcement para outputs do OllamaEvaluator.
Garante que o JSON gerado é válido e estruturado para consumo por pipeline de dados.

Uso: from schema_validator import validate_evaluation_output, EvaluationReport
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class EvaluationItem:
    """Schema de um item de avaliação — temperatura 0 para tasks estruturadas."""
    id: int
    prompt: str
    response: Optional[str]
    latency_seconds: float
    status: str  # "success" | "error"
    total_duration_ns: int = 0
    error_message: Optional[str] = None

    def __post_init__(self):
        if self.status not in ("success", "error"):
            raise ValueError(f"status inválido: {self.status!r}. Use 'success' ou 'error'.")
        if self.latency_seconds < 0:
            raise ValueError("latency_seconds não pode ser negativo.")


@dataclass
class ReportMetadata:
    """Metadados do relatório — schema enforcement (Mariana-Prompt)."""
    model: str
    timestamp: str
    total_prompts: int
    success_rate: str
    avg_latency_seconds: float

    def __post_init__(self):
        # Valida formato ISO 8601
        try:
            datetime.fromisoformat(self.timestamp)
        except ValueError:
            raise ValueError(f"timestamp inválido: {self.timestamp!r}. Use ISO 8601.")


@dataclass
class EvaluationReport:
    """
    Schema completo do relatório de avaliação.
    Anti-injection: nunca incluir inputs do usuário sem sanitização.
    """
    metadata: ReportMetadata
    evaluations: List[EvaluationItem] = field(default_factory=list)

    def to_json(self, indent: int = 4) -> str:
        """Serializa o relatório para JSON estruturado."""
        return json.dumps({
            "metadata": {
                "model": self.metadata.model,
                "timestamp": self.metadata.timestamp,
                "total_prompts": self.metadata.total_prompts,
                "success_rate": self.metadata.success_rate,
                "avg_latency_seconds": self.metadata.avg_latency_seconds,
            },
            "evaluations": [
                {
                    "id": e.id,
                    "prompt": e.prompt[:500],  # anti-injection: trunca prompt longo
                    "response": e.response,
                    "latency_seconds": e.latency_seconds,
                    "status": e.status,
                    "total_duration_ns": e.total_duration_ns,
                    **({"error_message": e.error_message} if e.error_message else {})
                }
                for e in self.evaluations
            ]
        }, indent=indent, ensure_ascii=False)


def validate_evaluation_output(raw_json: dict) -> EvaluationReport:
    """
    Valida e converte dict bruto para schema tipado.
    Mariana-Prompt: schema enforcement antes de persistir ou enviar para API.

    Raises:
        ValueError: se o schema estiver inválido
        KeyError: se campos obrigatórios estiverem ausentes
    """
    meta = raw_json["metadata"]
    metadata = ReportMetadata(
        model=meta["model"],
        timestamp=meta["timestamp"],
        total_prompts=meta["total_prompts"],
        success_rate=meta.get("success_rate", "N/A"),
        avg_latency_seconds=meta.get("avg_latency_seconds", 0.0),
    )

    evaluations = [
        EvaluationItem(
            id=item["id"],
            prompt=item["prompt"],
            response=item.get("response"),
            latency_seconds=item["latency_seconds"],
            status=item["status"],
            total_duration_ns=item.get("total_duration_ns", 0),
            error_message=item.get("error_message"),
        )
        for item in raw_json.get("evaluations", [])
    ]

    return EvaluationReport(metadata=metadata, evaluations=evaluations)
