# Auditoria Sofia-CIAO — Caipyra 2026
# Data: 2026-06-07 | Status: CONDICIONADO

---

## Veredito: ⚠️ CONDICIONADO

Projeto não está pronto para push público sem resolver os itens abaixo.
Nenhum blocker crítico de segurança. Bloqueios são de governança e qualidade.

---

## Blockers (resolver antes do push)

### 1. 🔴 Arquivos JSON temporários no workspace raiz
- `resposta_caipyra_*.json`, `resposta_pdi_*.json`, `chat_evento.json`, `chat_pdi.json`
- **Risco:** exposição de histórico de prompts + dados de carreira em repo público
- **Ação:** mover para `_temp/` (gitignored) ou deletar antes do commit

### 2. 🔴 `chrome_out.txt` no raiz
- Contém logs de sessão Chrome com remote debugging ativo
- **Risco:** baixo, mas não pertence ao repositório de aprendizados
- **Ação:** deletar ou gitignore

### 3. 🟡 `compare_repos.js` no raiz
- Script de debug temporário sem contexto documentado
- **Ação:** mover para `_temp/` ou deletar

### 4. 🟡 DAG Iceberg — `conn_id` hardcoded
- `conn_id="trino_production"` está fixo no código
- **Risco:** falha silenciosa se env diferente (staging vs prod)
- **Ação:** João-Backend parametrizar via variável de ambiente (ver abaixo)

### 5. 🟡 `stg_leads.sql` usa `SELECT *` no FROM renamed_and_cleaned
- Pedro-DBA: produção não aceita `SELECT *` sem LIMIT
- **Contexto:** é staging/view, ok para dbt, mas adicionar colunas explícitas é boa prática
- **Ação:** Pedro-DBA explicitará colunas no select final

---

## Condições para GO

- [ ] Limpar JSONs temporários + chrome_out.txt + compare_repos.js
- [ ] Parametrizar conn_id da DAG (João-Backend)
- [ ] Pedro-DBA: adicionar colunas explícitas ao stg_leads.sql final
- [ ] `.github/workflows/ci.yml` presente ✅
- [ ] `.gitignore` presente ✅
- [ ] `requirements.txt` presente ✅

---

## Riscos Residuais (pós-GO)

- Playwright CI roda headless mas depende de rede externa (practicetestautomation.com) — flaky risk baixo
- `evaluation_report.json` gerado pelo script não deve ser commitado (já no .gitignore ✅)
- dbt `dbt_utils.equal_rowcount` depende de `dim_users` que não existe no repositório — testes vão falhar em dbt run

---

## Aprovação final

**Sofia-CIAO:** Resolve os 5 itens → GO imediato.  
Sem necessidade de re-auditoria se as mudanças forem as listadas acima.
