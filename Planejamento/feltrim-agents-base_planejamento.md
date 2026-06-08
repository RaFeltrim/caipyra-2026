# Planejamento de Melhoria - feltrim-agents-base

## 📦 Nome do Projeto
**`feltrim-agents-base`** (Boilerplate Canônico do Feltrim Agents Framework - FF)

---

## 🔍 O Que o Projeto Faz
O projeto é a fundação para orquestração de múltiplos agentes de IA no ecossistema Feltrim. Ele define as regras de governança, protocolos de comunicação, rituais e um sistema estruturado de níveis e certificações para que agentes autônomos possam atuar em equipe de maneira coordenada, segura e auditável.

---

## 🛠️ Como Melhorá-lo
Podemos elevar a capacidade técnica do framework aplicando três pilares ensinados no Caipyra 2026:

### 1. PyTorch & Python Fluente (Orientação por Moacir A. Ponti)
* **Loops de Decisão Vetorizados**: Substituir verificações manuais de strings nos roteadores de mensagens por cálculo de similaridade de cosseno vetorizado em tensores utilizando modelos de embeddings rodando localmente (via PyTorch e Ollama).
* **Paradigmas de Python Fluente**:
  * Utilizar **Módulos Abstratos e Protocolos (`typing.Protocol`)** para definir interfaces de agentes desacopladas e elegantes.
  * Implementar **Mtodos Mágicos** (ex: `__call__` para executar uma iteração do agente, `__getitem__` para buscar histórico de memória).
  * Criar geradores (`yield`) para streaming assíncrono de respostas dos agentes.
* **Dataset & DataLoader**: Implementar `AgentHistoryDataset` e `AgentDataLoader` herdando de `torch.utils.data` para carregar, paralelizar (via *multiprocessing* nativo) e processar em lote logs históricos de conversações para treinamento de pequenos modelos locais ou sintonia de classificadores de rotas.

### 2. Dask (Processamento Distribuído)
* **Simulações Concorrentes Massivas**: Substituir loops de execução sequencial de agentes por tarefas paralelas usando a API de baixo nível `dask.delayed`. Isso permite paralelizar a execução de dezenas de agentes simultaneamente em pipelines de testes ou simulações sem gargalos de CPU/IO do interpretador CPython.

### 3. Apache Airflow (Orquestração de Fluxos de Longa Duração)
* **DAGs de Agentes**: Criar um compilador interno no framework capaz de exportar cadeias complexas de tarefas de agentes (ex: agente QA planeja -> agente Dev codifica -> agente Validador testa) em uma DAG do Apache Airflow. Isso trará:
  * Resiliência nativa com tratamento automático de falhas e retentativas (retries) com backoff exponencial.
  * Idempotência garantida usando o `execution_date` do Airflow para evitar execuções duplicadas e consumo desnecessário de tokens de LLM.
  * Monitoramento visual de dependências complexas.

---

## 🚀 Por Que Melhorá-lo
* **Alinhamento com PDI**: Fortalece as suas *hard skills* em engenharia de software avançada, modularização de IA e programação assíncrona/concorrente, preparando-o diretamente para testes e automações complexas com IA exigidos no time do Azure Data e nas pesquisas de pós-graduação no ICMC-USP.
* **Eficiência e Escala**: Transforma um boilerplate de orquestração local em um ecossistema pronto para produção, capaz de escalar para centenas de agentes rodando em paralelo sem perda de estabilidade ou controle de governança.
