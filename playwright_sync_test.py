from playwright.sync_api import sync_playwright, expect
import logging
from util.logging_config import setup_logging

setup_logging()

def test_google_search():
    search_text = "testing"  # Store the search text in a variable

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to Google
        page.goto("https://www.google.com")
        logging.info("Successfully loaded Google page: %s", page.title())
        
        # Wait for the search box to be visible and fill it with text
        search_box = page.locator("textarea[title='Search']")
        search_box.wait_for(state="visible")
        logging.info("Search box is visible. Typing text: '%s'", search_text)
        search_box.fill(search_text)
        
        # Press Enter to search
        page.keyboard.press("Enter")
        logging.info("Enter key pressed.")
        
        # Wait for the results to load by waiting for the Clear button to be visible
        clear_button = page.locator("#tsf [role='button'][aria-label='Clear']")
        clear_button.wait_for(state="visible")
        logging.info("Search results loaded. Clear button is visible.")
        
        # Get the text in the search box and verify it matches the expected value
        search_box_in_search_page = page.locator("#tsf [role='combobox'][aria-label='Search']")
        expect(search_box_in_search_page).to_be_visible()
        expect(search_box_in_search_page).to_have_text(search_text)
        logging.info("Assertion passed: Search box text matches the expected input.")
        # Take a screenshot of the search results page
        page.screenshot(path="google_search_results.png")
        
        # Close browser
        browser.close()
        logging.info("Browser closed successfully.")

test_google_search()
