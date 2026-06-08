# Planejamento de Melhoria - gestao_pedidos

## 📦 Nome do Projeto
**`gestao_pedidos`** (Order Management System Backend)

---

## 🔍 O Que o Projeto Faz
É um sistema backend em Python voltado para a gestão de pedidos de comércio eletrônico ou comercial, abrangendo o cadastro de clientes, inserção de itens, processamento de status do pedido (recebido, pago, faturado, enviado) e controle de estoque básico.

---

## 🛠️ Como Melhorá-lo
Podemos reestruturar a arquitetura do projeto e seus fluxos assíncronos aplicando as boas práticas de engenharia de software e processamento de dados do Caipyra 2026:

### 1. Clean Architecture e SOLID para Desacoplamento do Core
* **Refatoração Arquitetural**: Dividir a aplicação em quatro camadas claras e independentes de frameworks externos (como FastAPI ou Flask):
  * **Core Domain**: Entidades de negócio (ex: classe `Pedido`, `ItemPedido`, `Cliente`) e regras puras de validação, sem dependências de bancos de dados.
  * **Use Cases (Casos de Uso)**: Classes orquestradoras das ações do sistema (ex: `CriarPedidoUseCase`, `ProcessarPagamentoUseCase`), contendo a lógica de negócio explícita e regras de transição.
  * **Interface Adapters (Adaptadores)**: Repositórios concretos de acesso a dados (utilizando SQLAlchemy para PostgreSQL/MySQL) e controladores HTTP.
  * **Infrastructure & Frameworks**: Configurações de servidor web, conexões físicas de banco de dados e integrações externas.
* **Injeção de Dependências**: Garantir que as classes de alto nível não dependam de implementações de baixo nível (Princípio de Inversão de Dependência), facilitando testes unitários isolados com mocks rápidos.

### 2. Orquestração de Processos Assíncronos com Apache Airflow
* **Fluxo de Processamento de Pedido**: Um pedido pago dispara uma cadeia de eventos em segundo plano:
  1. Baixa de estoque no inventário.
  2. Emissão e registro da Nota Fiscal (faturamento).
  3. Solicitação de coleta junto à transportadora (logística).
  4. Disparo de e-mail de confirmação ao cliente.
* **Substituição de Threads Locais**: Migrar esse fluxo assíncrono para DAGs do **Apache Airflow**. Isso traz:
  * **Idempotência**: Garantia de que a tarefa de cobrança ou emissão de nota fiscal use o ID único do pedido como chave idempotente, evitando faturamento duplo no caso de falha de conexão com a API de pagamento.
  * **Tratamento de Falhas Resiliente**: Configurar retentativas automáticas (*retries*) com tempo de espera incremental para chamadas a APIs instáveis (como transportadoras ou gateway de pagamento).
  * **Monitoramento Visual**: Rastrear o andamento de cada etapa do pedido de forma centralizada e visual pelo painel do Airflow.

---

## 🚀 Por Que Melhorá-lo
* **Alinhamento com PDI & ICMC-USP**: O domínio de arquiteturas limpas (*Clean Architecture*) e princípios SOLID é um pré-requisito explícito nas disciplinas avançadas de desenvolvimento de software da USP e altamente valorizado em processos seletivos do Azure Engineering Team da Microsoft, onde o código limpo, extensível e testável é regra de sobrevivência.
* **Escalabilidade Industrial**: Evita que o backend sofra de gargalos de desempenho e falhas silenciosas ao gerenciar tarefas assíncronas em memória local, adotando o padrão de mercado para pipelines distribuídos e resilientes.
