import asyncio
from playwright.async_api import async_playwright

async def main():
    user_data_dir = r"C:\Users\Rafael Feltrim\AppData\Local\Google\Chrome\User Data"
    
    async with async_playwright() as p:
        print("Launching browser context...")
        try:
            # We use headless=False to show the browser to the user
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                args=["--start-maximized"]
            )
        except Exception as e:
            print(f"Error launching browser: {e}")
            return
            
        print("Browser launched. Opening page...")
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        try:
            await page.goto("https://gemini.google.com/app/7490dd66e56f8c06?hl=pt-BR", timeout=30000)
            print("Page loaded. Waiting for chat content...")
            
            # Wait for content to load
            await page.wait_for_timeout(10000)
            
            print("Scrolling to bottom...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)
            
            # Extract all text
            text = await page.evaluate("document.body.innerText")
            
            with open('gemini_chat_full.txt', 'w', encoding='utf-8') as f:
                f.write(text)
                
            print("Chat extracted successfully.")
        except Exception as e:
            print(f"Error during extraction: {e}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
