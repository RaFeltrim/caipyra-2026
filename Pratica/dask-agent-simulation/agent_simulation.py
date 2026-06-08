import time
import random
from dask import delayed

@delayed
def executar_agente_ia(agent_id: int, tarefa: str) -> dict:
    """Simula um agente autônomo resolvendo uma tarefa assíncrona (Ex: chamadas de LLM)."""
    tempo_processamento = random.uniform(1.2, 2.8)
    print(f"\n[Agente {agent_id}] Iniciando processamento da tarefa: '{tarefa}'")
    
    # Simula carga intensa de processamento de rede/I-O Bound
    time.sleep(tempo_processamento) 
    
    resultado = {
        "agente_id": agent_id,
        "tarefa": tarefa,
        "status": "Sucesso",
        "tempo_execucao": round(tempo_processamento, 2),
        "log": "Análise e triagem completas para a entrada de dados."
    }
    print(f"[Agente {agent_id}] Finalizado em {resultado['tempo_execucao']} segundos.")
    return resultado

@delayed
def consolidar_metricas(resultados_agentes: list) -> str:
    """Consolida as saídas calculadas em paralelo em um relatório estruturado unificado."""
    print("\n[Orquestrador] Coletando respostas e agregando métricas de execução...")
    time.sleep(0.4)
    
    linhas_relatorio = ["\n======= RELATÓRIO EXECUTIVO DE PIPELINES DE IA ======="]
    for res in resultados_agentes:
        linhas_relatorio.append(
            f"- Agente {res['agente_id']} executou em {res['tempo_execucao']}s | "
            f"Status: {res['status']} | Task: {res['tarefa']}"
        )
    linhas_relatorio.append("======================================================")
    return "\n".join(linhas_relatorio)


if __name__ == "__main__":
    # Definição das cargas de trabalho que entrarão no grafo direcionado acíclico (DAG)
    demandas = [
        "Avaliação de vulnerabilidades estruturais em scripts de automação",
        "Triagem orientada por LLM sobre logs críticos da pipeline",
        "Análise preditiva de falhas intermitentes em ambiente de staging",
        "Geração automatizada de relatórios sintáticos de cobertura de código"
    ]
    
    print("1. Montando o grafo computacional preguiçoso (Lazy Evaluation)...")
    
    # Criação da lista contendo os objetos Delayed intermediários
    tarefas_agentes = [
        executar_agente_ia(idx + 1, task) 
        for idx, task in enumerate(demandas)
    ]
    
    # A tarefa de consolidação herda a lista de promessas/tarefas futuras
    pipeline_final = consolidar_metricas(tarefas_agentes)
    
    print("2. Grafo estruturado com sucesso. Iniciando execução em paralelo via compute()...")
    tempo_inicial = time.time()
    
    # O Dask avalia as dependências e despacha as execuções concorrentes nos cores disponíveis
    relatorio_gerado = pipeline_final.compute()
    
    tempo_final = time.time()
    
    # Impressão do output consolidado
    print(relatorio_gerado)
    print(f"\nTempo total decorrido da operação: {round(tempo_final - tempo_inicial, 2)}s")
    print("(Note que o tempo total é muito menor que a soma dos tempos individuais dos agentes)")
