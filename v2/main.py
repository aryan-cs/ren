from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions

def main():
    # Instantiate ChromeOptions
    options = ChromeOptions()

    # Instantiate undetected Chrome driver with the configured options
    driver = Chrome(options=options)

    try:
        # Open the website
        driver.get("https://wrtn.ai")

        # Find the button element by class name and click it
        button = driver.find_element_by_class_name("css-0")
        button.click()

        # Do whatever you want here after clicking the button
        # For example, you can continue interacting with the site, perform further actions, etc.

    finally:
        # Keep the browser window open to continue interacting with the site
        input("Press Enter to close the browser...")

        # Close the browser window and terminate the driver
        driver.quit()

if __name__ == "__main__":
    main()