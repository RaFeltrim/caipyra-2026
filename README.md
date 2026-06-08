# Caipyra 2026 - Aprendizados e Apresentações

Este repositório foi criado para documentar os aprendizados, palestras, minicursos e o PDI (Plano de Desenvolvimento Individual) relacionados ao evento **Caipyra 2026**, organizando o conhecimento para futuras apresentações e profissionalização nos assuntos abordados.

---

## 📁 Estrutura de Pastas e Padrão de Organização

O repositório adota uma estrutura expandida para cobrir documentação, apresentação, plano de carreira (PDI), planejamentos de projetos e códigos práticos:

```text
Caipyra 2026/
├── README.md                          # Guia geral e visão geral do repositório
├── Referencias.md                     # Links úteis, livros e repositórios recomendados
├── Documentações/                     # Anotações e documentação das atividades
│   └── Palestra {N} - {Tema}/
│       └── {Assunto} - Documentação completa ({Tipo}).txt
├── Apresentacao/                      # Slides e roteiro de apresentação sobre o evento
│   ├── roteiro.md                     # Script de apoio para a apresentação
│   └── slides.pdf                     # Slides finais da apresentação
├── PDI/                               # Alinhamento das palestras com a sua carreira
│   ├── roadmap_conexao.md             # Como aplicar os aprendizados nos objetivos de PDI
│   ├── Rafael_Feltrim_CV.md           # Currículo profissional estruturado em inglês (ATS-optimized)
│   ├── microsoft_support_voucher.md   # Petição de suporte formal para reemissão de voucher (TDAH)
│   ├── entrevistas_preparacao.md      # Guia de narrativa de transição e acessibilidade
│   └── cv_generator/
│       └── generate_cv.py             # Script Weasyprint para gerar PDF do CV
├── Planejamento/                      # Planejamentos individuais de modernização de repositórios
│   ├── index.md                       # Índice de priorização e matriz de conceitos
│   └── {projeto}_planejamento.md      # Proposta de melhorias para cada repositório (6 projetos)
└── Pratica/                           # Códigos e projetos práticos desenvolvidos
    ├── dask-agent-simulation/         # Simulação de agentes de IA usando Dask
    ├── pytorch-event-encoder/         # Implementação de codificador de eventos em PyTorch
    ├── airflow-compaction/            # DAG de compactação de tabelas Apache Iceberg
    ├── dbt-analytics-crm/             # Pipeline dbt (staging, marts, schema)
    ├── prompt-evaluation-ollama/      # Avaliação local de prompts resiliente com Ollama
    └── playwright-resilience/         # Automação de testes resilientes com Playwright
```

### Detalhes de Uso e Exemplos para Cada Pasta

Para manter a consistência, cada diretório e arquivo possui um propósito definido e um exemplo prático de preenchimento:

#### 1. Arquivos na Raiz
* **`README.md`**: Centraliza a visão do repositório. Deve conter a estrutura geral e instruções de contribuição.
* **`Referencias.md`**: Armazena indicações de leitura, repositórios úteis e artigos indicados nas palestras.
  * *Exemplo de Uso:* Links de bibliotecas comentadas ou links para documentações oficiais do Python.

#### 2. Pasta `Documentações/`
* **Subpastas (`Palestra {N} - {Tema}/`)**: Organiza os aprendizados por ordem cronológica ou lógica de ocorrência no evento.
* **Arquivos (`{Assunto} - Documentação completa ({Tipo}).txt`)**: Guarda as anotações textuais detalhadas.
  * *Exemplo de Caminho:* `Documentações/Palestra 1 - Boas Práticas com Python/Clean Code - Documentação completa (Mini curso).txt`
  * *Exemplo de Caminho 2:* `Documentações/Palestra 2 - Inteligência Artificial/LLMs locais com Ollama - Documentação completa (Workshop).txt`

#### 3. Pasta `Apresentacao/`
* **`roteiro.md`**: Documento de apoio descrevendo o roteiro da sua fala por slide.
  * *Exemplo de Conteúdo:*
    ```markdown
    - Slide 1: Introdução (Falar sobre a importância do Caipyra 2026).
    - Slide 2: Principais temas abordados (Resumo das tracks de Python e IA).
    ```
* **`slides.pdf`**: O arquivo final de slides exportado para visualização rápida.

#### 4. Pasta `PDI/` (Plano de Desenvolvimento Individual)
* **`roadmap_conexao.md`**: Conecta as palestras assistidas com as suas metas profissionais.
* **[Rafael_Feltrim_CV.md](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/PDI/Rafael_Feltrim_CV.md)**: Currículo profissional estruturado em inglês otimizado para ATS.
* **[microsoft_support_voucher.md](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/PDI/microsoft_support_voucher.md)**: Chamado detalhado e fundamentado clinicamente para suporte da Microsoft.
* **[entrevistas_preparacao.md](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/PDI/entrevistas_preparacao.md)**: Roteiro e estratégia para entrevistas técnicas de alto impacto e requerimento de acessibilidade para TDAH.

#### 5. Pasta `Planejamento/`
* **`index.md`** e **`{projeto}_planejamento.md`**: Detalham como e por que aplicar os conceitos do Caipyra 2026 nos seus repositórios do GitHub.
  * *Exemplo de Caminho:* `Planejamento/feltrim-agents-base_planejamento.md` detalhando melhorias no framework de agentes com PyTorch e Airflow.

#### 6. Pasta `Pratica/`
* **[airflow-compaction/iceberg_compaction_dag.py](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/airflow-compaction/iceberg_compaction_dag.py)**: Compactação idempotente de Lakehouses.
* **[dbt-analytics-crm/](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/dbt-analytics-crm/)**: Pipeline dbt com modelos [stg_leads.sql](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/dbt-analytics-crm/models/staging/stg_leads.sql), [fct_sales_funnel.sql](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/dbt-analytics-crm/models/marts/fct_sales_funnel.sql) e testes de qualidade de dados.
* **[prompt-evaluation-ollama/prompt_evaluation.py](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/prompt-evaluation-ollama/prompt_evaluation.py)**: Avaliação resiliente de LLMs locais via Ollama com exponential backoff.
* **[playwright-resilience/resilient_playwright.py](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/playwright-resilience/resilient_playwright.py)**: Técnicas avançadas contra flaky tests (mocking de rede, localizadores de acessibilidade).

---

## 🚀 Como Contribuir

Sempre que adicionar um novo conteúdo, consulte este guia:

1. **Crie a pasta de documentação** em `Documentações/` usando a nomenclatura padrão com o número sequencial correspondente.
2. **Crie o arquivo de anotações** e adicione o tipo de atividade no nome do arquivo (ex: `(Palestra)`, `(Mini curso)`).
3. **Desenvolva os códigos práticos** correlacionados dentro da pasta `Pratica/`, usando nomes descritivos em minúsculas com hífen.
4. **Atualize o arquivo `Referencias.md`** se houver links ou bibliotecas relevantes indicadas na atividade.

