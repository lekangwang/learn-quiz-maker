from pyshadow.main import Shadow
from selenium.webdriver.common.by import By
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_section_names, parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, filter_questions_by_section, wait_until_page_fully_loaded
from .questions import Question_maker

# Is the path to the settings CSV file, please DO NOT TOUCH
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Navigate into each quiz section 
def create_quiz(driver):
    quiz_questions = parse_settings(MODULE_PATH, "/learn-quiz-template.csv")
    section_names = parse_section_names(quiz_questions)

    wait_until_page_fully_loaded(driver, 10)

    # Find iframe component with main quiz library content and switch webdriver to it
    main_iframe = driver.find_element(By.ID, "ctl_2")
    print(f"Main frame: {main_iframe}")
    driver.switch_to.frame(main_iframe)

    # Find frame component with main quiz library content and switch webdriver to it
    library_frames = driver.find_elements(By.TAG_NAME, "frame")
    print(f"Library frame: {library_frames}")
    driver.switch_to.frame(library_frames[-1])

    shadow_driver = Shadow(driver)

    section_link_elements = shadow_driver.find_elements(".d2l-link")

    # Navigate to each section listed the learn quiz template csv file
    for name in section_names:
        # Click on one of the 3 sections
        click_element_of_elements(section_link_elements, "Unit 01", "text")

        # Filter for all questions that belong to this unit in an array
        section_questions = filter_questions_by_section(name, quiz_questions)

        for question in section_questions:
            # print(f"{question}\n")
            # true_false_maker = Question_maker(driver)
            # true_false_maker.new_question("T/F")
            break

        # More logic HERE
        break

        # Find iframe component with main quiz library content and switch webdriver to it
        main_iframe = driver.find_element(By.ID, "ctl_2")
        print(f"Main frame: {main_iframe}")
        driver.switch_to.frame(main_iframe)

        # Find frame component with main quiz library content and switch webdriver to it
        library_frames = driver.find_elements(By.TAG_NAME, "frame")
        print(f"Library frame: {library_frames}")
        driver.switch_to.frame(library_frames[-1])

    # Focus driver back to whole DOM
    driver.switch_to.default_content()
        