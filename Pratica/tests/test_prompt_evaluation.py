"""
Testes Unitários — OllamaPromptEvaluator
Rafael-QA: caminho de falha primeiro, depois caminho feliz.
Cobertura mínima: 70% das linhas críticas.

Executar: pytest tests/test_prompt_evaluation.py -v
"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "prompt-evaluation-ollama"))
from prompt_evaluation import OllamaPromptEvaluator


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def evaluator():
    """Instância base do avaliador apontando para localhost mock."""
    return OllamaPromptEvaluator(host="http://localhost:11434", model="llama3")


@pytest.fixture
def sample_prompts():
    return [
        "Explique Clean Architecture em uma frase.",
        "O que é Shift-Left Testing?",
    ]


# ─────────────────────────────────────────────
# Rafael-QA: Caminhos de FALHA primeiro
# ─────────────────────────────────────────────

class TestFalhaCaminhosCriticos:
    """Testa comportamento do avaliador em cenários de falha."""

    def test_erro_de_conexao_retorna_status_error(self, evaluator, sample_prompts):
        """Se Ollama está offline, resultado deve ter status='error' (não raise)."""
        import requests

        with patch.object(evaluator.session, "post", side_effect=requests.exceptions.ConnectionError("Offline")):
            results = evaluator.evaluate_prompts(sample_prompts[:1])

        assert len(results) == 1
        assert results[0]["status"] == "error"
        assert results[0]["response"] is None
        assert "error_message" in results[0]

    def test_timeout_retorna_status_error(self, evaluator, sample_prompts):
        """Timeout deve ser capturado graciosamente."""
        import requests

        with patch.object(evaluator.session, "post", side_effect=requests.exceptions.Timeout("Timeout")):
            results = evaluator.evaluate_prompts(sample_prompts[:1])

        assert results[0]["status"] == "error"
        assert results[0]["latency_seconds"] >= 0

    def test_status_500_retorna_error(self, evaluator, sample_prompts):
        """HTTP 500 deve resultar em status='error'."""
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

        with patch.object(evaluator.session, "post", return_value=mock_response):
            results = evaluator.evaluate_prompts(sample_prompts[:1])

        assert results[0]["status"] == "error"

    def test_lista_vazia_retorna_lista_vazia(self, evaluator):
        """Nenhum prompt → nenhum resultado (sem exception)."""
        results = evaluator.evaluate_prompts([])
        assert results == []


# ─────────────────────────────────────────────
# Rafael-QA: Caminho Feliz
# ─────────────────────────────────────────────

class TestCaminhoFeliz:
    """Testa comportamento esperado em condições normais."""

    def _mock_success_response(self, prompt_text="Resposta mock"):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "response": prompt_text,
            "total_duration": 1_500_000_000
        }
        return mock_response

    def test_resultado_contem_campos_obrigatorios(self, evaluator, sample_prompts):
        """Cada resultado deve ter: id, prompt, response, latency, status."""
        with patch.object(evaluator.session, "post", return_value=self._mock_success_response()):
            results = evaluator.evaluate_prompts(sample_prompts)

        campos = {"id", "prompt", "response", "latency_seconds", "status", "total_duration_ns"}
        for r in results:
            assert campos.issubset(r.keys()), f"Campos faltando: {campos - r.keys()}"

    def test_ids_sao_sequenciais(self, evaluator, sample_prompts):
        """IDs devem ser 1, 2, 3... (não 0-indexed)."""
        with patch.object(evaluator.session, "post", return_value=self._mock_success_response()):
            results = evaluator.evaluate_prompts(sample_prompts)

        ids = [r["id"] for r in results]
        assert ids == list(range(1, len(sample_prompts) + 1))

    def test_status_success_em_resposta_valida(self, evaluator, sample_prompts):
        """Resposta HTTP 200 válida → status='success'."""
        with patch.object(evaluator.session, "post", return_value=self._mock_success_response()):
            results = evaluator.evaluate_prompts(sample_prompts[:1])

        assert results[0]["status"] == "success"
        assert results[0]["response"] == "Resposta mock"

    def test_latencia_positiva(self, evaluator, sample_prompts):
        """Latência deve ser um float positivo."""
        with patch.object(evaluator.session, "post", return_value=self._mock_success_response()):
            results = evaluator.evaluate_prompts(sample_prompts[:1])

        assert results[0]["latency_seconds"] >= 0.0


# ─────────────────────────────────────────────
# Rafael-QA: Geração de Relatório
# ─────────────────────────────────────────────

class TestSaveReport:
    """Testa geração do artefato JSON."""

    def test_report_gerado_com_metadata(self, evaluator, tmp_path):
        """Arquivo JSON deve conter chaves: metadata e evaluations."""
        results = [
            {"id": 1, "prompt": "p", "response": "r", "latency_seconds": 0.5,
             "status": "success", "total_duration_ns": 1000}
        ]
        output_file = str(tmp_path / "report.json")
        evaluator.save_report(results, output_file)

        with open(output_file, encoding="utf-8") as f:
            data = json.load(f)

        assert "metadata" in data
        assert "evaluations" in data
        assert data["metadata"]["model"] == "llama3"
        assert data["metadata"]["total_prompts"] == 1

    def test_report_contem_success_rate(self, evaluator, tmp_path):
        """Metadata deve incluir success_rate calculada."""
        results = [
            {"id": 1, "prompt": "p", "response": "r", "latency_seconds": 0.5,
             "status": "success", "total_duration_ns": 1000},
            {"id": 2, "prompt": "p2", "response": None, "latency_seconds": 0.1,
             "status": "error", "error_message": "timeout"},
        ]
        output_file = str(tmp_path / "report.json")
        evaluator.save_report(results, output_file)

        with open(output_file, encoding="utf-8") as f:
            data = json.load(f)

        assert "success_rate" in data["metadata"]
        assert data["metadata"]["success_rate"] == "50.0%"
