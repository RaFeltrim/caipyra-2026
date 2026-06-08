-- Pedro-DBA: Revisão completa do modelo stg_leads
-- Problema encontrado: SELECT * em produção sem colunas explícitas
-- Fix: colunas explícitas + comentário de schema contract

-- Materialização como view: correto para staging (leve, sem custo de storage)
{{ config(materialized='view') }}

WITH raw_source AS (
    -- Pedro-DBA: nunca SELECT * em tabelas de produção
    -- Declarar colunas usadas = schema contract explícito
    SELECT
        id,
        user_id,
        origin_source,
        current_status,
        expected_value,
        created_at,
        updated_at,
        is_test_account
    FROM {{ source('crm_raw', 'leads') }}
),

renamed_and_cleaned AS (
    SELECT
        -- Chaves com tipagem explícita (evita coerção implícita)
        CAST(id         AS STRING) AS lead_id,
        CAST(user_id    AS STRING) AS user_id,

        -- Texto normalizado: lowercase + trim (Pedro-DBA: índices em lowercase são menores)
        LOWER(TRIM(origin_source))  AS lead_source,
        LOWER(TRIM(current_status)) AS lead_status,

        -- Monetário: COALESCE antes do CAST (evita NULL propagation)
        COALESCE(CAST(expected_value AS NUMERIC), 0.0) AS estimated_revenue,

        -- Timestamps em UTC explícito (evita surpresas de fuso)
        CAST(created_at AS TIMESTAMP) AS created_at_utc,
        CAST(updated_at AS TIMESTAMP) AS updated_at_utc

    FROM raw_source
    -- Filtro de qualidade: exclui registros nulos e contas de teste
    WHERE id IS NOT NULL
      AND is_test_account = FALSE
)

-- Pedro-DBA: SELECT explícito no final — documenta o contrato de saída do modelo
SELECT
    lead_id,
    user_id,
    lead_source,
    lead_status,
    estimated_revenue,
    created_at_utc,
    updated_at_utc
FROM renamed_and_cleaned