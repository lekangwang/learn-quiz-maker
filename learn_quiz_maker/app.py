from learn_quiz_maker.helpers.driver import create_driver
from .navigation.login import login_user, navigate_to_course_quizzes
from .helpers.driver import create_driver
from time import sleep
from pyshadow.main import Shadow

# Initialize webdriver globally
driver = create_driver()
shadow_driver = Shadow(driver)

def run():
    login_user(driver)
    navigate_to_course_quizzes(shadow_driver, driver)
    sleep(5)
    driver.quit()



