from pyshadow.main import Shadow
from selenium.webdriver.common.by import By
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_section_names, parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, wait_until_page_fully_loaded

class Question_maker: 
    def __init__(self, driver):
        self.shadow_driver = Shadow(driver)
        self.driver = driver
    
    def switch_frame(self):
        # Find iframe component with main form content and switch webdriver to it
        main_iframe = self.driver.find_element(By.CSS_SELECTOR, ".d2l-fra-iframe>iframe")
        print(f"Main frame: {main_iframe}")
        self.driver.switch_to.frame(main_iframe)

        self.shadow_driver = Shadow(self.driver)
    
    def reset_frame(self):
        # Focus driver back to whole DOM
        self.driver.switch_to.default_content()

    def true_false(self, question_data):
        self.switch_frame()
        # Data extraction
        question_text = question_data["Question Text"]
        true_feedback = question_data["True Feedback"]
        false_feedback = question_data["False Feedback"]
        correct_answer = question_data["Correct Answer"]
        points = question_data["Points"]
        overall_feedback = question_data["Overall Feedback"]

        # Web elements declarations
        question_text_input = self.shadow_driver.find_element("")

        self.reset_frame()
    
    def multiple_choice(self, question_data):
        self.switch_frame()
        self.reset_frame()
    
    def multi_select(self, question_data):
        self.switch_frame()
        self.reset_frame()
    
    def written_answer(self, question_data):
        self.switch_frame()
        self.reset_frame()
    
    def short_answer(self, question_data):
        self.switch_frame()
        self.reset_frame()
    
    def matching(self, question_data):
        self.switch_frame()
        self.reset_frame()

    def fill_in_the_blanks(self, question_data):
        self.switch_frame()
        self.reset_frame()

    def ordered(self, question_data):
        self.switch_frame()
        self.reset_frame()

    def likert(self, question_data):
        self.switch_frame()
        self.reset_frame()
    
    # Creates a single question from start to finish
    def new_question(self, question_type, question_data):
        wait_until_page_fully_loaded(self.driver, 10)
        self.reset_frame()
        
        # Find iframe component with main quiz library content and switch webdriver to it
        main_iframe = self.driver.find_element(By.ID, "ctl_2")
        print(f"Main frame: {main_iframe}")
        self.driver.switch_to.frame(main_iframe)

        # Find frame component with main quiz library content and switch webdriver to it
        library_frames = self.driver.find_elements(By.TAG_NAME, "frame")
        print(f"Library frame: {library_frames}")
        self.driver.switch_to.frame(library_frames[-1])

        # Click on "New" button
        action_btns = self.shadow_driver.find_elements(".d2l-buttonmenu-text")
        print("From new_question")
        click_element_of_elements(action_btns, "New")

        sleep(1)

        # Click on new question button based on question type to get to the section form
        new_question_btns = self.shadow_driver.find_elements(".d2l-menu-item-text")
        for btn in new_question_btns:
            if btn.text != "":
                if btn.text.split(" ")[-1] == "(" + question_type + ")":
                    btn.click()
                    break
        
        # Call the appropriate function to fill the question form
        if question_type == "T/F":
            self.true_false(question_data)
        elif question_type ==  "MC":
            self.multiple_choice(question_data)
        elif question_type == "M-S":
            self.multi_select(question_data)
        elif question_type == "WR":
            self.written_answer(question_data)
        elif question_type == "SA":
            self.short_answer(question_data)
        elif question_type == "MAT":
            self.matching(question_data)
        elif question_type == "FIB":
            self.fill_in_the_blanks(question_data)
        elif question_type == "ORD":
            self.ordered(question_data)
        elif question_type == "LIK":
            self.likert(question_data)
        else:
            print("From new_question in Question_maker: No such question type was found!")