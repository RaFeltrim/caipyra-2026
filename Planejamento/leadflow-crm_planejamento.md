# Planejamento de Melhoria - leadflow-crm

## 📦 Nome do Projeto
**`leadflow-crm`** (LeadFlow CRM Web Application)

---

## 🔍 O Que o Projeto Faz
É uma aplicação web de CRM (Customer Relationship Management) desenvolvida com foco em gerenciamento de funis de vendas, rastreamento de oportunidades de negócios e engenharia de software com qualidade embutida (QA-focused).

---

## 🛠️ Como Melhorá-lo
Podemos transformar o LeadFlow CRM em um exemplo de alto nível de integração entre aplicação web, engenharia analítica de dados e qualidade de testes de ponta a ponta (E2E) aplicando os conceitos do Caipyra 2026:

### 1. Camada de Engenharia Analítica com dbt e Snowflake (ELT)
* **Extração & Carga (EL)**: Simular a carga das tabelas transacionais do CRM (como leads, contas, oportunidades de vendas e logs de contato) para um Data Warehouse na nuvem utilizando o Snowflake.
* **Transformação Inteligente com dbt**:
  * Implementar modelos de dados estruturados no **dbt** para construir o pipeline analítico do funil de vendas.
  * Estruturar a modelagem em camadas:
    * `Staging` (`stg_leads.sql`, `stg_opportunities.sql`): Limpeza e padronização básica dos tipos de dados de leads.
    * `Intermediate` (`int_lead_conversion_time.sql`): Lógica complexa para calcular o tempo médio de conversão entre etapas do funil.
    * `Mart` (`fct_sales_funnel.sql`, `dim_sales_agents.sql`): Tabelas fatos e dimensões prontas para consumo em dashboards do Power BI.
  * **Testes de Qualidade de Dados**: Definir no arquivo `schema.yml` testes automatizados do dbt para garantir integridade referencial, valores não nulos e ids de leads únicos.
  * **Linhagem de Dados**: Gerar o lineage graph automático do dbt para rastreabilidade de ponta a ponta do fluxo.

### 2. Automação E2E Resiliente com Playwright
* **Substituição de Testes Legados**: Garantir a estabilidade da aplicação web implementando uma suíte robusta de testes E2E com **Playwright** (aproveitando o suporte nativo a TypeScript).
* **Fluxos Críticos Automatizados**:
  * Criação e salvamento de novos leads com validação de dados de entrada.
  * Movimentação de cartões de leads (drag-and-drop) entre as colunas do Kanban de vendas e verificação do status atualizado.
  * Geração de relatórios de desempenho e carregamento de gráficos do pipeline.
* **Zero Flakiness**: Adotar seletores por texto visível (`getByRole`, `getByText`), esperas automáticas (*auto-waiting*) e estados de login reaproveitáveis (armazenando a sessão em arquivos JSON), mitigando totalmente falhas intermitentes (*flaky tests*).

---

## 🚀 Por Que Melhorá-lo
* **Alinhamento com PDI (Transição Azure Data Quality)**: O Microsoft Fabric e as posições modernas de engenharia no time da Azure demandam conhecimentos aprofundados sobre qualidade e transformação de dados analíticos (ELT) e integração entre sistemas transacionais (CRM) e analíticos. Unir dbt, Snowflake e Playwright no mesmo projeto demonstra total domínio sobre o ciclo completo dos dados e da qualidade de software.
* **Requisitos ICMC-USP**: O desenvolvimento estruturado de aplicações web com bancos de dados relacionais e analíticos se alinha perfeitamente com os projetos práticos de engenharia de software do ICMC-USP.
