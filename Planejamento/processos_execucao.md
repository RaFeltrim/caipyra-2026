# Log de Processos de Execução — Sessão Antigravity
> Registro de erros, tentativas e soluções durante a automação do projeto Caipyra 2026  
> **Data:** 2026-06-07 | **Agente:** Antigravity + Squad Feltrim

---

## 1. Abertura do Chrome com Remote Debugging

### Objetivo
Conectar o browser agent ao Chrome do usuário (já logado no Google) para extrair conteúdo do chat Gemini em: `https://gemini.google.com/app/7490dd66e56f8c06`

### Tentativas e Erros

| # | Comando | Erro | Causa |
|---|---------|------|-------|
| 1 | `chrome.exe --remote-debugging-port=9222 --user-data-dir=ChromeDebugProfile` | Browser agent não conectou | Perfil temporário sem sessão Google logada |
| 2 | `Start-Process chrome.exe` com perfil real + `Invoke-WebRequest localhost:9222` | `Impossível conectar-se ao servidor remoto` | Chrome subiu mas porta não vinculou a tempo (5s insuficiente) |
| 3 | Retry loop 5x com 3s de intervalo (35s total) | Todas as tentativas falharam | Chrome lançou em instância existente sem flags de debug |
| 4 | Diagnóstico: `Get-Process chrome`, `netstat :9222`, `SingletonLock` | 0 processos, porta livre, sem lock | Chrome não iniciou de forma alguma |

### Causa Raiz Identificada
O `Start-Process` lança o executável mas quando o Chrome já possui um **perfil em uso** ou quando o sistema tem configurações que bloqueiam o remote debugging (políticas de empresa, antivírus, flag `--remote-debugging-port` ignorada), o processo sobe sem vincular a porta.

### Solução Correta (Documentada para Reutilização)

**Passo 1 — Fechar Chrome completamente (verificar no Gerenciador de Tarefas)**
```powershell
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
```

**Passo 2 — Abrir Chrome manualmente via CMD como Administrador:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --remote-allow-origins=* ^
  --user-data-dir="C:\Users\Rafael Feltrim\AppData\Local\Google\Chrome\User Data" ^
  --no-first-run ^
  --start-maximized ^
  https://gemini.google.com/app/7490dd66e56f8c06?hl=pt-BR
```

**Passo 3 — Validar que a porta está ativa:**
```powershell
Invoke-WebRequest "http://localhost:9222/json" -UseBasicParsing | ConvertFrom-Json
```

**Passo 4 — Notificar o browser agent para conectar**

### Status Atual
- ⚠️ Chrome não conseguiu ser aberto programaticamente com debug nesta sessão
- ✅ Alternativa: usuário abre manualmente com o comando acima e notifica o agente
- ✅ Alternativa 2: usuário cola o texto das palestras diretamente no chat

---

## 2. Esgotamento de Quota dos Subagentes (429)

### Erro
```
RESOURCE_EXHAUSTED (code 429): Individual quota reached. 
Contact your administrator to enable overages. Resets in 2h27m38s.
```

### Afetados
- `agente_caipyra` (conv: `0a80a86a-88d3-4793-bafb-4336321c4404`)
- `browser` agent anterior (conv: `c67b2136-d366-452c-acd2-fe97cfb005da`)

### Causa
Excesso de chamadas de subagentes em curto período (múltiplas rodadas de análise + browser).

### Solução
- Aguardar reset (~2h27m a partir de ~17h12 BRT → ~19h39 BRT)
- Ou processar diretamente no agente principal (sem subagent) para economizar quota
- **Regra para próximas sessões:** máximo 2 subagentes ativos simultâneos

---

## 3. Arquivos Temporários no Workspace (Resolvido)

### Problema
Arquivos `resposta_caipyra_*.json`, `resposta_pdi_*.json`, `chat_*.json`, `chrome_out.txt`, `compare_repos.js` acumulados no raiz do workspace — flagados pela auditoria Sofia-CIAO como risco de exposição em repo público.

### Solução Aplicada
```powershell
Remove-Item -Path "resposta_caipyra*.json", "resposta_pdi*.json", "chat_evento.json", 
             "chat_pdi.json", "chrome_out.txt", "compare_repos.js" -Force
```
✅ **Resolvido em:** 2026-06-07

---

## 4. Subagente agente_caipyra — SELECT * em stg_leads.sql (Resolvido)

### Problema
`SELECT *` no CTE final do modelo dbt — viola regra Pedro-DBA de nunca `SELECT *` em produção.

### Solução Aplicada
Colunas explícitas declaradas no raw_source e no SELECT final.  
**Arquivo:** [stg_leads.sql](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/dbt-analytics-crm/models/staging/stg_leads.sql)  
✅ **Resolvido em:** 2026-06-07

---

## 5. DAG Iceberg — conn_id Hardcoded (Resolvido)

### Problema
`conn_id="trino_production"` fixo no código — falha silenciosa em ambientes staging.

### Solução Aplicada
```python
ICEBERG_CONN_ID = Variable.get("ICEBERG_CONN_ID", default_var="trino_staging")
```
**Arquivo:** [iceberg_compaction_dag.py](file:///c:/Users/Rafael%20Feltrim/Downloads/Caipyra%202026/Pratica/airflow-compaction/iceberg_compaction_dag.py)  
✅ **Resolvido em:** 2026-06-07

---

## Próximas Ações Pendentes

- [ ] Extrair conteúdo das 2 novas palestras do chat Gemini (bloqueado: Chrome debug / quota)
- [ ] Criar artefatos de Documentações/ e Pratica/ para as 2 novas palestras
- [ ] Commit e push do repositório Caipyra 2026 para o GitHub (Sofia: GO liberado)
