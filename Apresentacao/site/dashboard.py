import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="Caipyra 2026: Dashboard Interativo",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para forçar um visual premium e moderno
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
        color: #cbd5e1;
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        color: #ffffff !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.03);
    }
    div[data-testid="stMetricValue"] {
        color: #60a5fa !important;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Caipyra 2026: Dashboard de Evidências Técnicas")
st.write("Esta interface demonstra a evolução técnica e o paralelismo escalável utilizando conceitos do Caipyra, Dask, e Data Quality.")

# Sidebar
st.sidebar.image("../../Fotos/dask_scheduler_graph.png", use_container_width=True, caption="Task Graph Scheduler")
st.sidebar.header("Configurações do Simulador")
sim_speed = st.sidebar.slider("Velocidade da DAG (segundos/tarefa)", 0.1, 2.0, 0.5)
task_count = st.sidebar.slider("Quantidade de Tarefas na DAG", 5, 100, 30)

tab1, tab2, tab3 = st.tabs(["⚡ Computação Paralela (Dask)", "📊 Data Quality (Snowflake/dbt)", "🤝 Pessoas > Tecnologia"])

with tab1:
    st.header("Simulação de Execução: Dask Delayed vs Sequencial")
    st.write("O Dask constrói uma DAG (Grafo Acíclico Direcionado) para executar operações em paralelo, superando os gargalos de CPU/Memória do Python padrão.")
    
    col1, col2, col3 = st.columns(3)
    
    # Cálculos simulados
    seq_time = task_count * sim_speed
    dask_time = (task_count * sim_speed) / 8.0  # Simula 8 cores paralelos
    
    with col1:
        st.metric("Tempo Sequencial (Estimado)", f"{seq_time:.2f} s")
    with col2:
        st.metric("Tempo Dask Parallel (Simulado)", f"{dask_time:.2f} s")
    with col3:
        st.metric("Ganho de Otimização", f"{((seq_time - dask_time)/seq_time)*100:.1f} %")
        
    # Gráfico de Gantt Simulado de Tarefas executando em paralelo
    st.subheader("Simulação de Execução Paralela nas Threads do Processador")
    
    tasks = [f"Tarefa {i+1}" for i in range(task_count)]
    starts = []
    ends = []
    thread_ids = []
    
    # Distribui as tarefas em 8 threads virtuais
    for i in range(task_count):
        thread_id = i % 8
        starts.append(i // 8 * sim_speed)
        ends.append(starts[-1] + sim_speed)
        thread_ids.append(f"Thread {thread_id + 1}")
        
    df = pd.DataFrame({
        "Tarefa": tasks,
        "Início": starts,
        "Fim": ends,
        "Processamento": thread_ids
    })
    
    fig = go.Figure()
    
    colors = ["#3b82f6", "#10b981", "#fbbf24", "#f59e0b", "#8b5cf6", "#ec4899", "#14b8a6", "#6366f1"]
    
    for thread in sorted(df["Processamento"].unique()):
        df_thread = df[df["Processamento"] == thread]
        color_idx = int(thread.split()[-1]) - 1
        
        for idx, row in df_thread.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Fim"] - row["Início"]],
                y=[row["Processamento"]],
                base=[row["Início"]],
                orientation='h',
                name=row["Tarefa"],
                marker=dict(color=colors[color_idx % len(colors)]),
                showlegend=False,
                hovertemplate=f"<b>{row['Tarefa']}</b><br>Início: {row['Início']:.2f}s<br>Fim: {row['Fim']:.2f}s"
            ))
            
    fig.update_layout(
        title="Cronograma de Ocupação de CPU (Multi-threading)",
        xaxis_title="Tempo de Execução (segundos)",
        yaxis_title="Instâncias de Processamento",
        height=400,
        barmode='stack',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#ffffff")
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Métricas de Data Quality & Integridade (dbt + Snowflake)")
    st.write("Abaixo simulamos a volumetria e auditoria de qualidade de tabelas carregadas no data lakehouse.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        rows_processed = st.number_input("Volume de registros diários", 10000, 1000000, 250000)
    with c2:
        error_rate = st.slider("Taxa simulada de inconsistência (%)", 0.0, 5.0, 0.2, step=0.1)
    with c3:
        st.write("")
        st.write("")
        run_tests = st.button("Executar Testes de Qualidade")
        
    if run_tests:
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            
        failures = int(rows_processed * (error_rate / 100.0))
        
        st.write("")
        if failures == 0:
            st.success("🎉 dbt test concluído com sucesso. 0 falhas encontradas em 6 asserções de integridade.")
        else:
            st.error(f"❌ dbt test falhou! Encontrados {failures} registros órfãos ou duplicados que violaram as restrições da schema.yml.")
            st.info("Recomendação: Verifique os logs do stg_leads para depuração de integridade referencial.")

with tab3:
    st.header("A Filosofia Humana: Pessoas > Tecnologia")
    st.write("""
    Nas equipes de QA e engenharia da **Foursys**, o principal motor de inovação é o elemento humano. 
    As ferramentas e tecnologias integradas no Caipyra servem para apoiar as pessoas no seu trabalho do dia a dia, 
    minimizando tarefas burocráticas e exaustivas para liberar espaço para a criatividade e a resolução de problemas complexos.
    """)
    
    st.subheader("Rituais Culturais no QA Studio:")
    st.markdown("""
    * **Code Review Colaborativo**: Disseminação de conhecimento em vez de controle punitivo.
    * **Shift-Left**: Antecipar testes e participar do refinamento do design ajuda o time a construir a qualidade de forma orgânica.
    * **Acomodação de TDAH/Acessibilidade**: Criar espaços acolhedores e apoiar a neurodiversidade fortalece a pluralidade de ideias e soluções.
    """)
    
    st.image("../../Fotos/WhatsApp Image 2026-06-08 at 13.07.43.jpeg", width=600, caption="Visualização do auditório do evento - Conexões e Networking")
