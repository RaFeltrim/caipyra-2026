# Site de Apresentação Caipyra 2026 ➔ QA Studio Foursys

Este diretório contém a aplicação web de apresentação e simulação interativa construída para compartilhar os conhecimentos adquiridos no **Caipyra 2026** (ICMC-USP) com o time de **QA Studio da Foursys**.

O projeto é estruturado sob o lema **Pessoas > Tecnologia**, demonstrando como as ferramentas apoiam a colaboração, a neurodiversidade (TDAH) e as automações robustas.

---

## 🛠️ Arquitetura do Projeto

1. **Front-end / Interatividade**:
   - **Tailwind CSS + daisyUI**: Design System premium em dark mode com tokens de cores e layouts responsivos prontos de alta qualidade.
   - **HTMX**: Atualizações parciais de HTML no lado do servidor (SSR) sem a necessidade de frameworks JavaScript pesados (SPA).
2. **Back-end / Servidores**:
   - **Flask (`app.py`)**: Roteamento principal do site de slides e endpoints de simulação HTMX (resiliência de testes e mapeamento de mainframe).
   - **Streamlit (`dashboard.py`)**: Interface de dados interativa para simular o paralelismo de grafos de tarefas (Dask) e monitoramento de cargas Snowflake/dbt.

---

## 📁 Estrutura de Pastas
```text
Apresentacao/site/
├── app.py             # Servidor Web Flask (Rotas & HTMX endpoints)
├── dashboard.py       # Dashboard de simulação interativa em Streamlit
├── requirements.txt   # Dependências Python específicas do site
├── templates/         # Templates Jinja2 do Flask
│   ├── base.html      # Layout estrutural global (Tailwind + daisyUI + HTMX)
│   ├── index.html     # Slides de trilhas técnicas e visão do evento
│   ├── mainframe.html # Painel de mapeamento de mainframe (Gemini)
│   └── live_coding.html # Playground de interações parciais HTMX
└── README.md          # Este arquivo de instruções
```

---

## 🚀 Como Iniciar Localmente

### 1. Preparar o Ambiente
Crie e ative um ambiente virtual Python, e instale as dependências:

```bash
# Navegar até a pasta do site
cd "Apresentacao/site"

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Rodar o Site de Apresentação (Flask)
Inicie o servidor local do Flask:

```bash
python app.py
```
Acesse o site interativo no navegador em: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### 3. Rodar o Dashboard de Simulações (Streamlit)
Inicie a aplicação do Streamlit em outro terminal (com o ambiente virtual ativo):

```bash
streamlit run dashboard.py
```
Acesse a simulação do Dask e Snowflake no navegador em: **[http://localhost:8501](http://localhost:8501)**

---

## 🤖 Mapeamento de Mainframe
O site integra um aliado configurado no **Google Gemini** para mapeamento e modernização de legados JCL e Copybook COBOL:
🔗 **[Aliado Gemini para Automação de Mainframe](https://gemini.google.com/app/7c16b3363b152ba1?hl=pt-BR)**
