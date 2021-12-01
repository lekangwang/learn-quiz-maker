from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pyshadow.main import Shadow
from time import sleep

# Helper function to click an certain element given 
# a collection of elements
def click_element_of_elements(elements, innertext, mode=None):
    # Check if element has a text property or a text HTML attribute
    if not elements[0].text == "" or mode == "text":
        print(f"click_element_of_elements (text): {innertext}")

        # Click the element if the text property matches
        for el in elements:
            if el.text == innertext:
                el.click()
                break
    else:
        print(f"click_element_of_elements (attribute): {innertext}")

        # Click the element if the text HTML attribute matches
        for el in elements:
            if el.get_attribute('text') == innertext:
                el.click()
                break

# Executes some JS to ensure that the HTML is fully rendered before any automated interactions
def wait_until_page_fully_loaded(driver, wait_time):
    WebDriverWait(driver, wait_time).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

# For debugging purposes, prints the length and contents of a collection of elements
def about(elements, var_name):
    # Print the array of elements and the number of elements
    print(f"{var_name}: {elements}")
    print(f"{var_name} length: {len(elements)}")

    # Print the text inside each element 
    for (i, el) in enumerate(elements):
        if not el.text == "":
            print(f"Element {i + 1} text: {el.text}")
        else:
            print(f"Element {i + 1} text: {el.get_attribute('text')}")

# Specific to create_quiz, filters questions based on section name
def filter_questions_by_section(section_name, quiz_questions):
    section_questions = []

    # Loop through all quiz questions and filter by section name
    for question in quiz_questions:
        if question["Section"] == section_name:
            section_questions.append(question)

    return section_questions



