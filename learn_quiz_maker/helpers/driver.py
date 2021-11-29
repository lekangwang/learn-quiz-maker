from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Webdriver manager will automatically install the 
# correct driver software for your Chrome version
from webdriver_manager.chrome import ChromeDriverManager

# Create a webdriver object with the correct driver software installed
def create_driver():
    chrome_options = Options()

    # Debug chrome window version
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver
