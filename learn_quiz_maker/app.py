from learn_quiz_maker.helpers.driver import create_driver
from .navigation.login import login_user
from .helpers.driver import create_driver

# Initialize webdriver globally to prevent shut down
driver = create_driver() 

def run():
    # parse_settings()
    login_user(driver)


