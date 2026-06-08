{{ config(
    materialized='incremental',
    unique_key='funnel_operation_id',
    incremental_strategy='merge'
) }}

WITH leads AS (
    SELECT * FROM {{ ref('stg_leads') }}
),

-- Suposição de uma dimensão existente para enriquecimento e validação de chaves estrangeiras
users_dim AS (
    SELECT * FROM {{ ref('dim_users') }}
),

funnel_aggregation AS (
    SELECT
        -- Geração de chave substituta única para a granularidade da tabela fato
        {{ dbt_utils.generate_surrogate_key(['leads.lead_id', 'leads.lead_status']) }} AS funnel_operation_id,
        
        leads.lead_id,
        leads.user_id,
        leads.lead_source,
        leads.lead_status,
        leads.estimated_revenue,
        leads.created_at_utc AS valid_from_timestamp
        
    FROM leads
    INNER JOIN users_dim ON leads.user_id = users_dim.user_id
    
    {% if is_incremental() %}
    -- Filtro de corte incremental para otimização de varredura (idempotência operacional)
    WHERE leads.updated_at_utc >= (SELECT MAX(valid_from_timestamp) FROM {{ this }})
    {% endif %}
)

SELECT * FROM funnel_aggregation