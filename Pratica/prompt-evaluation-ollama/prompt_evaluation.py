"""
Prompt Evaluation Pipeline — Ollama (Local LLM)
================================================
Caipyra 2026 | Prática: Resiliência em Engenharia de Dados

Conceitos aplicados:
- Exponential Backoff via urllib3.Retry (evita falha silenciosa)
- Logging estruturado para auditoria em esteiras CI/CD
- Coleta de métricas de latência por inferência
- Relatório JSON como artefato de pipeline

Dependências: pip install requests urllib3
Uso: python prompt_evaluation.py
"""

import json
import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from pathlib import Path
from typing import List, Dict, Any

# Configuração de log para auditoria clara na esteira CI/CD
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("OllamaEvaluator")


class OllamaPromptEvaluator:
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama3"):
        self.api_url = f"{host}/api/generate"
        self.model = model
        self.session = self._build_resilient_session()

    def _build_resilient_session(self) -> requests.Session:
        """
        Constrói uma sessão HTTP com Exponential Backoff.
        Essencial para evitar quebras por instabilidade momentânea do serviço local.

        Tempos de espera entre tentativas: 1s → 2s → 4s → 8s
        """
        session = requests.Session()
        retries = Retry(
            total=4,
            backoff_factor=2,  # Espera: 1s, 2s, 4s, 8s entre tentativas
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def evaluate_prompts(
        self,
        prompts: List[str],
        temperature: float = 0.7,
        seed: int = 42
    ) -> List[Dict[str, Any]]:
        """
        Executa a inferência em lote, capturando métricas de latência.

        Args:
            prompts: Lista de prompts a serem avaliados
            temperature: Temperatura do modelo (0.0 = determinístico, 1.0 = criativo)
            seed: Semente para reprodutibilidade dos resultados

        Returns:
            Lista de dicionários com resultados, latência e status de cada prompt
        """
        results = []
        logger.info(
            f"Iniciando avaliação de {len(prompts)} prompts no modelo "
            f"'{self.model}' (Temp: {temperature}, Seed: {seed})."
        )

        for idx, prompt in enumerate(prompts, 1):
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "seed": seed
                }
            }

            logger.info(f"Processando prompt {idx}/{len(prompts)}...")
            start_time = time.perf_counter()

            try:
                response = self.session.post(self.api_url, json=payload, timeout=60)
                response.raise_for_status()

                latency = time.perf_counter() - start_time
                data = response.json()

                results.append({
                    "id": idx,
                    "prompt": prompt,
                    "response": data.get("response", "").strip(),
                    "latency_seconds": round(latency, 3),
                    "status": "success",
                    "total_duration_ns": data.get("total_duration", 0)
                })
                logger.info(f"✅ Sucesso. Latência: {latency:.2f}s")

            except requests.exceptions.RequestException as e:
                latency = time.perf_counter() - start_time
                logger.error(f"❌ Falha ao processar prompt {idx}: {str(e)}")
                results.append({
                    "id": idx,
                    "prompt": prompt,
                    "response": None,
                    "latency_seconds": round(latency, 3),
                    "status": "error",
                    "error_message": str(e)
                })

        success_count = sum(1 for r in results if r["status"] == "success")
        logger.info(
            f"Avaliação concluída: {success_count}/{len(results)} prompts bem-sucedidos."
        )
        return results

    def save_report(
        self,
        results: List[Dict[str, Any]],
        output_file: str = "evaluation_report.json"
    ) -> None:
        """
        Gera o artefato final em JSON para consumo pela esteira CI/CD.

        Args:
            results: Lista de resultados da avaliação
            output_file: Caminho do arquivo de saída
        """
        output_path = Path(output_file)
        avg_latency = (
            sum(r["latency_seconds"] for r in results) / len(results)
            if results else 0
        )

        with output_path.open("w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "model": self.model,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "total_prompts": len(results),
                    "success_rate": f"{sum(1 for r in results if r['status'] == 'success') / len(results) * 100:.1f}%",
                    "avg_latency_seconds": round(avg_latency, 3)
                },
                "evaluations": results
            }, f, indent=4, ensure_ascii=False)
        logger.info(f"📄 Relatório salvo com sucesso em: {output_path.absolute()}")


if __name__ == "__main__":
    # Prompts de teste — cobrindo Clean Architecture, BDD e Playwright
    test_prompts = [
        "Explique o conceito de Clean Architecture em uma frase.",
        "Gere um cenário BDD em Gherkin para o login de um usuário.",
        "Qual a principal vantagem de usar Playwright sobre Selenium?"
    ]

    evaluator = OllamaPromptEvaluator(model="llama3")
    evaluation_results = evaluator.evaluate_prompts(test_prompts, temperature=0.3)
    evaluator.save_report(evaluation_results)
