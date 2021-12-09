from pyshadow.main import Shadow
from selenium.webdriver.common.by import By
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_section_names, parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, filter_questions_by_section, focus_on_library_homepage, wait_until_page_fully_loaded
from .questions import Question_maker

# Is the path to the settings CSV file, please DO NOT TOUCH
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Navigate into each quiz section and create quiz questions using the Question_maker class
def create_quiz(driver):
    quiz_questions = parse_settings(MODULE_PATH, "/learn-quiz-template.csv")

    # Retreive from the quiz csv file, all unique section names
    section_names = parse_section_names(quiz_questions)

    wait_until_page_fully_loaded(driver, 10)

    # LOCATION: QUIZ LIBRARY HOMEPAGE, SWITCH DRIVER TO IT
    focus_on_library_homepage(driver)

    # Navigate to each section listed the learn quiz template csv file
    for name in section_names:
        # Create new shadow driver and find all sections visible on the quiz library homepage
        shadow_driver = Shadow(driver)
        section_link_elements = shadow_driver.find_elements(".d2l-link")
        # Click on the section element on the quiz library homepage
        # that matches the name of the section found in the quiz csv file
        # for the current loop iteration
        # click_element_of_elements(section_link_elements, "Unit 01", "text")
        click_element_of_elements(section_link_elements, name, "text")

        # Filter for all questions that belong to this unit into an array
        section_questions = filter_questions_by_section("Unit 01", quiz_questions)
        # section_questions = filter_questions_by_section(name, quiz_questions)

        for question in section_questions:
            print(f"Current question in inner loop: {question}\n")

            # Initalizes a new question maker object and creates a new question
            # as specified in the function call using question["Type"]
            maker = Question_maker(driver)
            maker.new_question(question["Type"], question)
            # maker.new_question("T/F", question)
            sleep(3)
            # break
            # maker.new_question("FIB", question)

        # break
        # Go back to the main homepage 
        focus_on_library_homepage(driver)
        question_library_link = shadow_driver.find_element("a.d2l-link.d2l-link-small")
        question_library_link.click()
        wait_until_page_fully_loaded(driver, 10)
        sleep(1)

    # Focus driver back to whole DOM
    driver.switch_to.default_content()
        