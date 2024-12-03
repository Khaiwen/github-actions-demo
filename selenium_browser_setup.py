import argparse
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Selenium Google search test.")
    parser.add_argument("--browser", type=str, default="chrome", help="Name of the browser to use")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    args = parser.parse_args()
    driver = launch_browser(args.browser, args.headless)