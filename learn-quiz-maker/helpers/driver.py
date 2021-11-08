from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

# Initialize and return a web driver object 
def create_driver ():
    chromedriver_link = "https://chromedriver.chromium.org/downloads"
    chromeversion_link = "chrome://settings/help"

    # Check if the chromedriver.exe file exists
    if (not os.path.isfile("../chromedriver")):
        # Error message
        print("chromedrive.exe does not exist.")
        print(f"Check your browser version here: {chromeversion_link}")
        print(f"Please download the correct chromedriver file corresponding to your browser version at: {chromedriver_link}")
        return None

    # Initialize a new web driver object
    service_obj = Service("../chromedriver")
    driver = webdriver.Chrome(service=service_obj)

    # Check the user's Chrome & chromedriver.exe version
    browser_version = driver.capabilities["browserVersion"].split(".")[0]
    driver_version = driver.capabilities["chrome"]["chromedriverVersion"].split(".")[0]

    if browser_version != driver_version:
        # Close the driver/test session 
        driver.quit()
        print("Triggered")

        # Error message
        print("Your chromedriver.exe file does not match your version of Chrome")
        print(f"Your Chrome browser version: {browser_version}, chromedriver.exe version: {driver_version}")
        print(f"Please download the correct chromedriver file corresponding to your browser version at: {chromedriver_link}")
        return None
    else:
        return driver

