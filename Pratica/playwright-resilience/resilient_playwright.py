"""
Automação E2E Resiliente com Playwright — Anti-Flaky
======================================================
Caipyra 2026 | Prática: Shift-Left Testing & Qualidade de Dados

Conceitos aplicados:
- Mocking de rotas de rede ANTES da navegação (interceptação de API)
- Locadores baseados em acessibilidade (get_by_role, get_by_label)
- Auto-waiting nativo do Playwright (sem time.sleep!)
- Tratamento de múltiplas abas/popups
- Screenshot automático em falha (evidência para CI/CD)

Dependências: pip install playwright && playwright install chromium
Uso: python resilient_playwright.py
"""

import asyncio
import logging
from playwright.async_api import async_playwright, Page, expect, Route

# Configuração de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("E2E_Playwright")


async def mock_login_api(route: Route) -> None:
    """
    Intercepta e simula a resposta da API de autenticação.

    Por que mockar? Isola o teste do frontend de instabilidades do backend
    ou banco de dados — fundamento do Shift-Left Testing.
    Em ambientes de dados, isso equivale a mockar uma API de ingestão.
    """
    logger.info("🔀 Interceptando chamada de rede: POST /api/v1/login")
    await route.fulfill(
        status=200,
        content_type="application/json",
        json={"token": "mocked_jwt_token_12345", "user": {"id": 1, "name": "QA Executivo"}}
    )


async def test_realistic_e2e_flow() -> None:
    """
    Fluxo E2E completo demonstrando as boas práticas do Caipyra 2026:
    1. Mocking de API antes da navegação
    2. Locadores por acessibilidade (não XPath frágil)
    3. Auto-waiting sem sleep()
    4. Tratamento de popups/novas abas
    5. Screenshot em falha como evidência CI/CD
    """
    async with async_playwright() as p:
        # headless=False para demonstração visual; use True em CI/CD
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True
        )
        page = await context.new_page()

        try:
            # =========================================================
            # ETAPA 1: Configurar Mocking ANTES da navegação
            # Vital para eliminar flaky tests causados por APIs de terceiros
            # =========================================================
            await page.route("**/api/v1/login", mock_login_api)

            logger.info("🌐 Navegando para o sistema de teste...")
            await page.goto("https://practicetestautomation.com/practice-test-login/")

            # =========================================================
            # ETAPA 2: Locadores Robustos Baseados em Acessibilidade
            # Evite XPath ou CSS complexos — localize como um usuário real.
            # Conexão com Data Quality: assim como validamos semântica de dados,
            # validamos semântica da UI (labels, roles, não seletores CSS frágeis).
            # =========================================================
            logger.info("✍️ Preenchendo formulário de login...")
            await page.get_by_label("Username").fill("student")
            await page.get_by_label("Password").fill("Password123")

            # =========================================================
            # ETAPA 3: Interação com o elemento correto (role-based)
            # =========================================================
            await page.get_by_role("button", name="Submit").click()

            # =========================================================
            # ETAPA 4: Espera Inteligente (Auto-waiting nativo)
            # expect() faz retry automático até o timeout.
            # NUNCA use await asyncio.sleep(X) — isso é um anti-pattern!
            # =========================================================
            logger.info("✅ Validando transição de estado pós-login...")
            await expect(
                page.get_by_text("Logged In Successfully")
            ).to_be_visible(timeout=5000)
            await expect(
                page.get_by_role("link", name="Log out")
            ).to_be_visible()

            # =========================================================
            # ETAPA 5: Tratamento de Popups e Múltiplas Abas
            # Padrão comum em testes de dashboards de dados (ex: Fabric, Metabase)
            # =========================================================
            logger.info("🪟 Simulando abertura de nova aba dinâmica...")
            async with page.expect_popup() as new_page_info:
                # Em produção, clique no elemento que abre a aba;
                # aqui injetamos via JS para demonstrar a mecânica
                await page.evaluate("window.open('https://example.com', '_blank');")

            new_page = await new_page_info.value
            await new_page.wait_for_load_state("networkidle")  # Espera a rede estabilizar

            logger.info(f"✅ Nova aba carregada: '{await new_page.title()}'")
            await expect(
                new_page.get_by_role("heading")
            ).to_contain_text("Example Domain")

            logger.info("🎉 Teste E2E finalizado com estabilidade garantida.")

        except Exception as e:
            # Em CI/CD real: attach screenshot + Playwright trace como evidência
            logger.error(f"❌ Falha na execução do teste: {e}")
            await page.screenshot(path="falha_e2e_trace.png")
            logger.info("📸 Screenshot de falha salvo: falha_e2e_trace.png")
            raise e

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    # Python requer um event loop para rodar a API assíncrona do Playwright
    asyncio.run(test_realistic_e2e_flow())
