from pyshadow.main import Shadow
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, wait_until_page_fully_loaded

# Is the path to the settings CSV file, please DO NOT TOUCH
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Navigate to the quiz library of the course
def navigate_to_quiz_library(shadow_driver, driver):
    wait_until_page_fully_loaded(driver, 10)

    # Find all quiz tabs
    quiz_tabs = shadow_driver.find_elements(".d2l-tool-areas-link")
    # print(f"Quiz tabs length: {len(quiz_tabs)}")
    # for tab in quiz_tabs:
    #     print(f"Quiz tab text: {tab.get_attribute('text')}")
    #     print(f"Quiz tag name: {tab.tag_name}")
    click_element_of_elements(quiz_tabs, "Question Library")

    wait_until_page_fully_loaded(driver, 10)

    print("navigate_to_quiz_library: Navigated to quiz library!")

# Create a new quiz section and navigate into it
# This function runs depending on settings.csv
def navigate_to_section_form(driver):
    settings = parse_settings(MODULE_PATH, "/settings.csv")
    new_section = settings["NewSection"].lower()

    # Exit the function if the user doesn't want a section made
    if new_section == "no":
        return

    wait_until_page_fully_loaded(driver, 10)

    # Find iframe component with main quiz library content and switch webdriver to it
    main_iframe = driver.find_element(By.ID, "ctl_2")
    print(f"Main frame: {main_iframe}")
    driver.switch_to.frame(main_iframe)

    # Find frame component with main quiz library content and switch webdriver to it
    library_frames = driver.find_elements(By.TAG_NAME, "frame")
    print(f"Library frame: {library_frames}")
    driver.switch_to.frame(library_frames[-1])

    # Create a new shadow webdriver with the new webdriver that is focused on the appropriate <frame> tag
    shadow_driver = Shadow(driver)

    # Find both "New" and "Import" buttons in the quiz library and click "New"
    library_btns = shadow_driver.find_elements(".d2l-action-buttons-item")
    click_element_of_elements(library_btns, "New")
    
    # Wait for dropdown options to appear
    sleep(2)

    # Find all drop down options under "New" and click
    # "Section"
    dropdown_options = shadow_driver.find_elements("d2l-menu-item")
    click_element_of_elements(dropdown_options, 'Section')

    # Focus driver back to whole DOM
    driver.switch_to.default_content()

    print("navigate_to_section_form: Section form reached!")

def create_section(driver):
    settings = parse_settings(MODULE_PATH, "/settings.csv")
    new_section = settings["NewSection"].lower()
    section_title = settings["SectionName"]
    section_title = settings["SectionText"]
    section_shuffle = settings["Shuffle"].lower()

    # Exit the function if the user doesn't want a section made
    if new_section == "no":
        return
    
    # Set section_shuffle to True/False
    if section_shuffle == "no":
        section_shuffle = False
    else:
        section_shuffle = True

    # Wait for New Section form to appear
    sleep(4)
    
    # Find iframe component with main form content and switch webdriver to it
    main_iframe = driver.find_element(By.TAG_NAME, "iframe")
    print(f"Main frame: {main_iframe}")
    driver.switch_to.frame(main_iframe)

    # Create a new shadow webdriver with the new webdriver that is focused on the appropriate <frame> tag
    shadow_driver = Shadow(driver)

    # Find title_input and input title (from settings.csv)
    section_title_input = shadow_driver.find_element("#qed-title")
    section_text_input = shadow_driver.find_element(".d2l-htmleditor-inline-html-block.d2l-input")
    section_shuffle_checkbox = shadow_driver.find_element("#qed-section-shuffle")
    section_save_btn = shadow_driver.find_element(".primary[name='Submit']")

    section_title_input.click()
    section_title_input.send_keys(section_title)

    section_text_input.click()
    section_text_input.send_keys(section_title)

    if section_shuffle:
        section_shuffle_checkbox.click()

    section_save_btn.click()

    # Focus driver back to whole DOM
    driver.switch_to.default_content()
    print("create_section: Quiz section created!")

