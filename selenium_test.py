# To execute this test, run the following command: 
# python selenium_test.py --browser chrome --headless

import argparse
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Set up logging configuration with detailed format and timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def configure_browser_options(browser_name, headless, window_size="1920,1080"):
    """Configures browser-specific options."""
    options = None
    match browser_name:
        case "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless=new")
                options.add_argument(f"--window-size={window_size}")
        case "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument(f"--width={window_size.split(',')[0]}")
                options.add_argument(f"--height={window_size.split(',')[1]}")
        case "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument(f"--window-size={window_size}")
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")
    return options

def launch_browser(browser_name, headless, window_size="1920,1080"):
    """Launches the specified browser."""
    options = configure_browser_options(browser_name, headless, window_size)
    match browser_name:
        case "chrome":
            driver = webdriver.Chrome(options=options)
        case "firefox":
            driver = webdriver.Firefox(options=options)
        case "edge":
            driver = webdriver.Edge(options=options)
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")
    
    if not headless:
        driver.maximize_window()
    logging.info("Running test on %s browser.", browser_name)
    return driver

# Function to test Google search using Selenium
def test_selenium_google_search(browser_name, headless):
    # Store the search text in a variable
    search_text = "testing selenium"  

    # Launch the browser based on the browser name provided
    driver = launch_browser(browser_name, headless)

    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        logging.info("Successfully loaded Google page: %s", driver.title)

        # Wait for the search box to be visible and fill it with text
        search_box = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[title='Search']"))
        )
        search_box.send_keys(search_text)
        logging.info("Typed text: '%s'", search_text)

        # Press Enter to search
        search_box.send_keys(Keys.RETURN)
        logging.info("Enter key pressed.")

        # Wait for the search results to load by waiting for the Clear button to be visible
        clear_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tsf [role='button'][aria-label='Clear']"))
        )
        clear_button.is_displayed()
        logging.info("Search results loaded. Clear button is visible.")

        # Get the text in the search box and verify it matches the expected value
        search_box_in_search_page = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tsf [role='combobox'][aria-label='Search']"))
        )
        assert search_box_in_search_page.is_displayed(), "Search box is not visible"
        actual_search_text = search_box_in_search_page.get_attribute("value")
        assert actual_search_text == search_text, \
            f"Expected '{search_text}' but found '{actual_search_text}' in the search box"
        logging.info("Search box text matches the expected input.")

        driver.save_screenshot(f"google_search_results_{browser_name}.png")
        logging.info("Screenshot saved.")

    finally:
        # Close the browser
        driver.quit()
        logging.info("Browser closed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Selenium Google search test.")
    parser.add_argument("--browser", type=str, default="chrome", help="Name of the browser to use")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    args = parser.parse_args()

    test_selenium_google_search(args.browser, args.headless)
