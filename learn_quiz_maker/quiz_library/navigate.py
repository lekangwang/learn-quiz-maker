from pyshadow.main import Shadow
from selenium.webdriver.common.by import By
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_section_names, parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, focus_on_library_homepage, wait_until_page_fully_loaded

# Is the path to the settings CSV file, please DO NOT TOUCH
MODULE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

# Navigate to the quiz library of the course
def navigate_to_quiz_library(shadow_driver, driver):
    wait_until_page_fully_loaded(driver, 10)
    sleep(1)

    # Find all quiz tabs and click "Question Library"
    quiz_tabs = shadow_driver.find_elements(".d2l-tool-areas-link")
    click_element_of_elements(quiz_tabs, "Question Library")

    print("navigate_to_quiz_library: Navigated to quiz library!")

# Navigates from the quiz libary main menu to 
# a new section form
def navigate_to_section_form(driver):
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

    section_link_elements = shadow_driver.find_elements(".d2l-link")
    for s in section_link_elements:
        print(s.text)

    # Find both "New" and "Import" buttons in the quiz library and click "New"
    library_btns = shadow_driver.find_elements(".d2l-buttonmenu-text")
    click_element_of_elements(library_btns, "New")

    sleep(1)

    # Find all drop down options under "New" and click
    # "Section"
    dropdown_options = shadow_driver.find_elements(".d2l-menu-item-text")
    click_element_of_elements(dropdown_options, "Section", "text")

    # Focus driver back to whole DOM
    driver.switch_to.default_content()
    print("navigate_to_section_form: Section form reached!")

# Loops through sections.csv file
# creates and saves each section
def create_sections(driver):
    settings = parse_settings(MODULE_PATH, "/sections.csv")

    # Exit the function if there are no sections to be made
    if len(settings) == 0:
        return
    
    for section in settings:
        navigate_to_section_form(driver)
        section_title = section["SectionName"]
        section_shuffle = section["Shuffle"].lower()
        section_text = section["SectionText"]

        # Set section_shuffle to True/False
        if section_shuffle == "no":
            section_shuffle = False
        else:
            section_shuffle = True

        # Wait for New Section form to appear
        sleep(3)
        
        # Find iframe component with main form content and switch webdriver to it
        main_iframe = driver.find_element(By.CSS_SELECTOR, ".d2l-fra-iframe>iframe")
        print(f"Main frame: {main_iframe}")
        driver.switch_to.frame(main_iframe)

        # Create a new shadow webdriver with the new webdriver that is focused on the appropriate <frame> tag
        shadow_driver = Shadow(driver)

        # Find title_input and input title (from settings.csv)
        section_title_input = shadow_driver.find_element("#qed-title")
        section_shuffle_checkbox = shadow_driver.find_element("#qed-section-shuffle")
        section_save_btn = shadow_driver.find_element(".primary[type=\"submit\"]")

        # Enter the title of the new section
        section_title_input.click()
        section_title_input.send_keys(section_title)

        # Enable shuffling if requested in settings.csv
        if section_shuffle:
            section_shuffle_checkbox.click()

        # First click on the input div containing the input iframe
        # div_input_container = driver.find_element(By.CSS_SELECTOR, ".qed-d2l-htmleditor-container[label=\"Section Text \"]")
        div_input_container = shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Section Text\"]")
        div_input_container.click()
        div_input_container.send_keys(section_text)

        # Click the save button
        section_save_btn.click()

        # Wait until the quiz libary main menu is loaded
        sleep(3)

        # Focus driver back to whole DOM
        driver.switch_to.default_content()
        print("create_section: Quiz section created!")

# Automatically place the newly created sections at the top 
def shift_sections_to_top(driver):
    settings = parse_settings(MODULE_PATH, "/sections.csv")
    
    focus_on_library_homepage(driver)

    shadow_driver = Shadow(driver)
    # Click on "Order" in library main menu
    order_btn = shadow_driver.find_element("d2l-button-subtle[text=\"Order\"]")
    order_btn.click()
    wait_until_page_fully_loaded(driver, 10)
    sleep(2)

    num_sections = len(settings)   
    # print(f"num_sections: {num_sections}")

    # Newly created sections are always going 
    # to be at the bottom of the section list
    sections_checkboxes = shadow_driver.find_elements("input[type=\"checkbox\"]")
    # print(f"sections: {len(sections_checkboxes)}")
    shift_up_btn = shadow_driver.find_element("button[title=\"Move Up\"]")
    save_btn = shadow_driver.find_element("#z_a")
    num_shift = len(sections_checkboxes) - num_sections

    # print(f"num_shift: {num_shift}")

    # Click on all newly created sections
    for i in range(len(sections_checkboxes) - 1, len(sections_checkboxes) - num_sections - 1, -1):
        sections_checkboxes[i].click()
    
    # Shift up the new sections to the top
    for i in range(num_shift):
        shift_up_btn.click()

    driver.execute_script("arguments[0].scrollIntoView();", save_btn)
    save_btn.click()

    wait_until_page_fully_loaded(driver, 10)
    
    # Focus driver back to whole DOM
    driver.switch_to.default_content()
    print("shift_sections_to_top: New Sections Shifted!")



    