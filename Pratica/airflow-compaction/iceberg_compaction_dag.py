"""
DAG: Iceberg Compaction — Hardened
João-Backend: conn_id parametrizado via Airflow Variable (sem hardcode)
Pedro-DBA: macros de data corrigidas (sintaxe Airflow 2.x)
Beatriz-TL: alertas de falha ativados para rastreabilidade em produção

Uso: configurar Airflow Variable "ICEBERG_CONN_ID" com o valor correto
     (ex: "trino_production" em prod, "trino_staging" em staging)
"""

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

# João-Backend: nunca hardcode de conn_id
# Usar Airflow Variable → sem if/else de ambiente no código
ICEBERG_CONN_ID = Variable.get("ICEBERG_CONN_ID", default_var="trino_staging")
ICEBERG_TABLE   = Variable.get("ICEBERG_TABLE",   default_var="analytics.event_logs")
ICEBERG_CATALOG = Variable.get("ICEBERG_CATALOG", default_var="prod_catalog")

# Beatriz-TL: alertas ativados — sem silêncio em produção
default_args = {
    "owner": "data_engineering",
    "depends_on_past": True,       # idempotência temporal garantida
    "email_on_failure": True,       # alerta obrigatório em produção
    "email_on_retry": False,
    "email": ["rafael@feltrim.dev"],
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="iceberg_binary_compaction",
    default_args=default_args,
    description="Compactação idempotente de tabelas Apache Iceberg — hardened",
    schedule_interval="@daily",
    start_date=datetime(2026, 6, 1),
    catchup=True,
    max_active_runs=1,
    tags=["iceberg", "optimization", "production"],
) as dag:

    # Task 1: Compactação de small files com sort strategy
    # Pedro-DBA: 512MB por arquivo = sweet spot para Trino/Spark
    compact_iceberg_table = SQLExecuteQueryOperator(
        task_id="optimize_iceberg_compaction",
        conn_id=ICEBERG_CONN_ID,
        sql=f"""
            CALL {ICEBERG_CATALOG}.system.rewrite_data_files(
                table => '{ICEBERG_TABLE}',
                options => map(
                    array['max_file_size_bytes', 'strategy'],
                    array['536870912', 'sort']
                ),
                where => 'event_timestamp >= TIMESTAMP ''{{{{ data_interval_start }}}}''
                          AND event_timestamp < TIMESTAMP ''{{{{ data_interval_end }}}}'''
            );
        """,
    )

    # Task 2: Expirar snapshots antigos
    # Pedro-DBA: retain_last=10 garante time-travel de ~10 dias úteis
    # João-Backend: macro ds_add correta para Airflow 2.x
    expire_iceberg_snapshots = SQLExecuteQueryOperator(
        task_id="expire_old_snapshots",
        conn_id=ICEBERG_CONN_ID,
        sql=f"""
            CALL {ICEBERG_CATALOG}.system.expire_snapshots(
                table => '{ICEBERG_TABLE}',
                older_than => TIMESTAMP '{{{{ macros.ds_add(ds, -7) }}}} 00:00:00',
                retain_last => 10
            );
        """,
    )

    # Task 3: Otimizar manifests (João-Backend: reduz overhead de planejamento de query)
    rewrite_manifests = SQLExecuteQueryOperator(
        task_id="rewrite_manifests",
        conn_id=ICEBERG_CONN_ID,
        sql=f"""
            CALL {ICEBERG_CATALOG}.system.rewrite_manifests(
                table => '{ICEBERG_TABLE}'
            );
        """,
    )

    # Fluxo: compactar → expirar snapshots → otimizar manifests
    compact_iceberg_table >> expire_iceberg_snapshots >> rewrite_manifests