from selenium import webdriver

# Webdriver manager will automatically install the 
# correct driver software for your Chrome version
from webdriver_manager.chrome import ChromeDriverManager

# Create a webdriver object with the correct driver software installed
def create_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver
