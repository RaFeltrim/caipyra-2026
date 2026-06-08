from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Cache simulado de logs de erro para demonstração de QA
SIMULATED_ERRORS = [
    {"id": "ERR001", "type": "Flaky Test", "desc": "Timeout exception on Selenium click due to page latency", "recommendation": "Migrate locator to accessibility-based Playwright locator."},
    {"id": "ERR002", "type": "Schema Failure", "desc": "Model fct_sales_funnel unique constraint failed", "recommendation": "Implement unique test constraint on schema.yml and audit stg_leads staging merge."},
    {"id": "ERR003", "type": "Compaction Lag", "desc": "Trino Iceberg query slow - thousands of small manifest files", "recommendation": "Trigger iceberg_compaction_dag.py DagRun via Airflow scheduler."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mainframe")
def mainframe():
    return render_template("mainframe.html")

@app.route("/live-coding")
def live_coding():
    return render_template("live_coding.html")

# ==========================================
# HTMX PARTIAL ENDPOINTS (Server-Side HTML)
# ==========================================

@app.route("/htmx/check-pipeline", methods=["POST"])
def check_pipeline():
    # Simulando um pequeno delay para testar o loading indicator do HTMX
    time.sleep(1)
    status = request.form.get("status", "healthy")
    
    if status == "healthy":
        alert_class = "alert-success"
        message = "✅ Todos os pipelines dbt/Snowflake estão em conformidade. Testes de integridade aprovados!"
    else:
        alert_class = "alert-error"
        message = "❌ Falha de consistência detectada em stg_leads. 3 registros duplicados identificados."
        
    return f"""
    <div class="alert {alert_class} shadow-lg transition-all duration-300">
        <div>
            <span>{message}</span>
        </div>
    </div>
    """

@app.route("/htmx/mainframe-prompt", methods=["POST"])
def mainframe_prompt():
    time.sleep(1.2)
    prompt_input = request.form.get("prompt", "")
    
    if not prompt_input.strip():
        return """
        <div class="alert alert-warning">
            <span>Por favor, insira um prompt válido para análise.</span>
        </div>
        """
    
    # Simula resposta estruturada do aliado Gemini para mapeamento de legados
    return f"""
    <div class="bg-slate-900 border border-slate-700 rounded-lg p-5 shadow-inner space-y-4">
        <div class="flex items-center justify-between border-b border-slate-700 pb-3">
            <span class="text-xs font-semibold text-sky-400 uppercase tracking-wider">Mapeamento de Legados via Gemini</span>
            <span class="badge badge-success text-xs">Análise Concluída</span>
        </div>
        <p class="text-sm text-slate-300 italic font-mono">"Processando prompt: '{prompt_input}'..."</p>
        <div class="space-y-2 text-sm">
            <h4 class="font-bold text-white">📋 Recomendações do Aliado IA:</h4>
            <ul class="list-disc pl-5 space-y-1 text-slate-300">
                <li><strong>Mapeamento de Fluxo JCL:</strong> Identificado JOB <code>QA_RUN_MAIN</code> com dependência em 3 arquivos sequenciais VSAM.</li>
                <li><strong>Cenários de Teste Gerados:</strong> 5 asserções BDD (Gherkin) para validar a consistência das saídas em fitas legadas.</li>
                <li><strong>Dica de Automação:</strong> Mockar chamadas de API do mainframe usando o módulo de interceptação de rede Playwright.</li>
            </ul>
        </div>
        <div class="text-right">
            <a href="https://gemini.google.com/app/7c16b3363b152ba1?hl=pt-BR" target="_blank" class="btn btn-sm btn-outline btn-info">Abrir Aliado Gemini</a>
        </div>
    </div>
    """

@app.route("/htmx/qa-insight", methods=["GET"])
def qa_insight():
    insight_type = request.args.get("type", "pytest")
    
    if insight_type == "playwright":
        title = "Resiliência com Playwright"
        details = "Migração de Selenium para Playwright reduziu flaky tests em 75% usando accessibility-based locators e mocking de requisições de rede."
    elif insight_type == "dask":
        title = "Paralelismo no QA"
        details = "Dask distribui massas de teste de carga em paralelo, convertendo tarefas demoradas em uma DAG de execução distribuída assíncrona."
    else:
        title = "Pessoas > Tecnologia"
        details = "O principal ativo de um time de QA é a comunicação objetiva e empatia (Cultura de Code Review). Ferramentas apoiam rituais, mas rituais apoiam pessoas."

    return f"""
    <div class="card bg-slate-800 border border-slate-700 shadow-xl">
        <div class="card-body">
            <h3 class="card-title text-sky-400 font-bold text-lg">{title}</h3>
            <p class="text-sm text-slate-300">{details}</p>
        </div>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
