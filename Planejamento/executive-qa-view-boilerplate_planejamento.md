# Planejamento de Melhoria - executive-qa-view-boilerplate

## 📦 Nome do Projeto
**`executive-qa-view-boilerplate`** (Offline Executive QA Dashboard Boilerplate)

---

## 🔍 O Que o Projeto Faz
Trata-se de um painel executivo offline para visualização de métricas de qualidade de software (QA), contendo dados estatísticos de suítes de testes, taxas de aprovação, falhas recorrentes e sugestões de melhorias simuladas (mocked AI insights) em formato de dashboard interativo.

---

## 🛠️ Como Melhorá-lo
Podemos transformar este boilerplate em uma ferramenta de produção inteligente e integrada a esteiras de desenvolvimento modernas usando os seguintes conceitos do Caipyra 2026:

### 1. Ingestão Dinâmica de Relatórios Playwright
* **Substituição de Mock Data**: Desenvolver um analisador (parser) em Python para ler e estruturar os resultados de execução reais gerados pelo **Playwright** (lendo o arquivo `report.json` gerado pelo comando `playwright test --reporter=json`).
* **Visualização Avançada**: Atualizar a interface do dashboard para renderizar dinamicamente gráficos de tendência de tempo de execução das suítes de teste, histórico de testes flutuantes (*flaky*) e taxas de sucesso de rotas específicas.

### 2. Triagem Inteligente de Logs com LLMs Locais (CI/CD)
* **Pipeline de IA para Diagnóstico de Falhas**: Implementar uma esteira automática em Python (usando Ollama e o modelo local Llama-3/Gemma-2) para analisar testes que falharam.
* **Fluxo de Trabalho**:
  1. O Playwright roda na esteira e detecta um teste falho.
  2. Um script em Python captura o log de falha (stack trace), a mensagem de erro e a URL da tela.
  3. O script envia um prompt estruturado para o Ollama local solicitando:
     * Classificação da falha: bug real, alteração de seletor UI, timeout de rede ou teste flutuante (*flaky*).
     * Sugestão concisa de correção em português.
  4. O resultado gerado pela IA é salvo diretamente no banco do dashboard e exibido em um card destacado "Diagnóstico de IA" na tela do respectivo teste falhado.
* **Python Fluente no Script de Integração**:
  * Escrever o script de triagem utilizando classes limpas, tipagem estática robusta, loops assíncronos (`asyncio`) para consultar o Ollama e gerenciar concorrência de chamadas à API, e gerenciadores de contexto para ler/escrever arquivos temporários de logs com segurança.

---

## 🚀 Por Que Melhorá-lo
* **Alinhamento com PDI (Orquestração de IA na CI/CD)**: Conecta-se de forma direta com seu plano estratégico de implementar LLMs locais para triagem automática em esteiras de teste. Essa melhoria serve como um case prático e de grande impacto técnico para apresentar ao time de Engenharia de Dados/Qualidade do Azure Data na Microsoft, demonstrando capacidade de inovação e controle rigoroso de qualidade em CI/CD.
* **Demonstração Prática**: Leva o projeto de um simples dashboard estático mockado para uma ferramenta real de observabilidade de testes com inteligência artificial integrada, impressionando recrutadores e parceiros de negócio.
