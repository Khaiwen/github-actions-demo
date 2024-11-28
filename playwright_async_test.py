import asyncio
from playwright.async_api import async_playwright

async def test_google_search():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        print(await page.title())
        await browser.close()

asyncio.run(test_google_search())