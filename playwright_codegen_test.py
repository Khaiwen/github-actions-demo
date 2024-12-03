# This code is generated using Playwright codegen tool

from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("automation step by step")
    page.keyboard.press("Enter")
    page.locator("h3").filter(has_text="Automation Step by Step: NEVER STOP LEARNING").click()
    page.get_by_text("Home").click()

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)