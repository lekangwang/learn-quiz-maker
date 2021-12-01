from learn_quiz_maker.helpers.driver import create_driver
from learn_quiz_maker.quiz_library.navigate import create_sections, navigate_to_quiz_library, navigate_to_section_form
from .navigation.login import login_user, navigate_to_course_quizzes
from .helpers.driver import create_driver
from .quiz_library.quiz import create_quiz
from pyshadow.main import Shadow

# Initialize a global webdriver
driver = create_driver()
executor_url = driver.command_executor._url
session_id = driver.session_id

# Initialize a global shadow webdriver
shadow_driver = Shadow(driver)

# Main function that is where all app operations happen
# at a high level
def run():
    # login_user(driver)
    # navigate_to_course_quizzes(shadow_driver, driver)
    # navigate_to_quiz_library(shadow_driver, driver)
    create_sections(driver)
    # create_quiz(driver)

    # # Close the Chrome session after 5 seconds
    # sleep(120)
    # driver.quit()



