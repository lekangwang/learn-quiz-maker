from pyshadow.main import Shadow
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep
import os
from learn_quiz_maker.helpers.parsers import parse_csv_round_braces, parse_section_names, parse_settings
from learn_quiz_maker.helpers.util import about, click_element_of_elements, focus_on_library_homepage, wait_until_page_fully_loaded

class Question_maker: 
    def __init__(self, driver):
        self.shadow_driver = Shadow(driver)
        self.driver = driver
    
    # When a question form is visible, switch driver to the form iframe
    def switch_frame(self):
        # Find iframe component with main form content and switch webdriver to it
        main_iframe = self.driver.find_element(By.CSS_SELECTOR, ".d2l-fra-iframe>iframe")
        print(f"Main frame: {main_iframe}")
        self.driver.switch_to.frame(main_iframe)

        self.shadow_driver = Shadow(self.driver)
    
    # Reset driver to focus on the whole HTML document
    def reset_frame(self):
        # Focus driver back to whole DOM
        self.driver.switch_to.default_content()

    def true_false(self, question_data):
        self.switch_frame()

        print(f"From true_false, received data dict: {question_data}")

        # Data extraction
        # Text
        question_text = question_data["Question Text"]
        true_feedback = question_data["True Feedback"]
        false_feedback = question_data["False Feedback"]
        correct_answer = question_data["Correct Answer"].lower()
        points = question_data["Points"]
        overall_feedback = question_data["Overall Feedback"]

        # Web elements declarations
        question_text_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Question Text\"]")
        true_feedback_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label=\"Feedback Answer True feedback\"]")
        false_feedback_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label=\"Feedback Answer False feedback\"]")
        overall_feedback_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Overall Feedback\"]")
        default_points_input = self.shadow_driver.find_element("#qed-points")
        correct_answer_input = None
        save_btn = self.shadow_driver.find_element("button[name=\"Submit\"]")

        if correct_answer == "true":
            correct_answer_input = self.shadow_driver.find_element("input[aria-label=\"Answer True is correct\"]")
        else:
            correct_answer_input = self.shadow_driver.find_element("input[aria-label=\"Answer False is correct\"]")

        # Fill in T/F fields
        question_text_input.click()
        question_text_input.send_keys(question_text)

        true_feedback_input.click()
        true_feedback_input.send_keys(true_feedback)

        false_feedback_input.click()
        false_feedback_input.send_keys(false_feedback)

        correct_answer_input.click()

        self.driver.execute_script("arguments[0].scrollIntoView();", overall_feedback_input) 
        overall_feedback_input.click()
        overall_feedback_input.send_keys(overall_feedback)

        self.driver.execute_script("arguments[0].scrollIntoView();", save_btn)
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)
     
        save_btn.click()
        self.reset_frame()
    
    def multiple_choice(self, question_data):
        self.switch_frame()

        print(f"From multiple_choice, received data dict: {question_data}")

        # Data extraction
        # Text
        question_text = question_data["Question Text"]
        overall_feedback = question_data["Overall Feedback"]
        # Number
        num_options = int(question_data["Number of Options"])
        correct_answer = int(question_data["Correct Answer"])
        points = int(question_data["Points"])
        # Boolean
        randomize = lambda choice : bool(choice == "yes")
        randomize = randomize(question_data["Randomize"].lower())
        print(f"randomize: {randomize}")
        # List
        option_text = parse_csv_round_braces(question_data["Options Text"])
        feedback_text = parse_csv_round_braces(question_data["Feedback on Options"])

        # First clear all options (except for the last one)
        option_remove_btns = self.shadow_driver.find_elements(".remove.icon-button")
        print(f"option_remove_btns length: {len(option_remove_btns)}")
        for btn in option_remove_btns[:-1]:
            btn.click()
            sleep(1) # Wait until webpage elements stop moving

        # Add enough options to match num_options (specified by csv file)
        add_answer_btn = self.shadow_driver.find_element(".d2l-button-subtle-content")
        for i in range(num_options - 1):
            add_answer_btn.click()
            sleep(1)

        # Web element declarations
        question_text_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Question Text\"]")
        option_text_inputs = self.shadow_driver.find_elements(".qed-d2l-htmleditor-container[label^=\"Answer\"]")
        feedback_text_inputs = self.shadow_driver.find_elements(".qed-d2l-htmleditor-container[label^=\"Feedback\"]")
        answer_checkboxes = self.shadow_driver.find_elements("input[aria-label^=\"Answer\"]")
        randomize_checkbox = self.shadow_driver.find_element("#qed-randomize-answers")
        overall_feedback_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Overall Feedback\"]")
        default_points_input = self.shadow_driver.find_element("#qed-points")
        save_btn = self.shadow_driver.find_element(".primary[name=\"Submit\"]")

        # Fill in MC form
        question_text_input.click()
        question_text_input.send_keys(question_text)

        for i in range(len(option_text)):
            self.driver.execute_script("arguments[0].scrollIntoView();", option_text_inputs[i]) 
            option_text_inputs[i].click()
            option_text_inputs[i].send_keys(option_text[i])
            feedback_text_inputs[i].click()
            feedback_text_inputs[i].send_keys(feedback_text[i])

        answer_checkboxes[correct_answer - 1].click()

        self.driver.execute_script("arguments[0].scrollIntoView();", randomize_checkbox) 
        if randomize == True:
            randomize_checkbox.click()
        
        self.driver.execute_script("arguments[0].scrollIntoView();", overall_feedback_input) 
        overall_feedback_input.click()
        overall_feedback_input.send_keys(overall_feedback)
        
        self.driver.execute_script("arguments[0].scrollIntoView();", save_btn) 
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        save_btn.click()
        self.reset_frame()
    
    def multi_select(self, question_data):
        self.switch_frame()

        print(f"From multi-select, received data dict: {question_data}")

        # Data extraction
        # Text
        question_text = question_data["Question Text"]
        grading_method = question_data["Grading Method"].lower()
        # Numbers
        num_options = int(question_data["Number of Options"])
        points = int(question_data["Points"])
        # Boolean
        randomize = lambda choice : bool(choice == "yes") 
        randomize = randomize(question_data["Randomize"].lower())
        # List
        options_text = parse_csv_round_braces(question_data["Options Text"])
        correct_answers = parse_csv_round_braces(question_data["Correct Answer"])
        correct_answers = [int(val) for val in correct_answers]

        # Clear all existing option inputs except for 1
        # First clear all options (except for the last one)
        option_remove_btns = self.shadow_driver.find_elements(".remove.icon-button")
        print(f"option_remove_btns length: {len(option_remove_btns)}")
        for btn in option_remove_btns[:-1]:
            btn.click()
            sleep(1) # Wait until webpage elements stop moving

        # Add option inputs according to num_options
        add_answer_btn = self.shadow_driver.find_element(".d2l-button-subtle-content")
        for i in range(num_options - 1):
            add_answer_btn.click()
            sleep(1)

        # Web element declarations
        question_text_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Question Text\"]")
        option_text_inputs = self.shadow_driver.find_elements(".qed-d2l-htmleditor-container[label^=\"Answer\"]")
        answer_checkboxes = self.shadow_driver.find_elements("input[aria-label^=\"Answer\"]")
        randomize_checkbox = self.shadow_driver.find_element("#qed-randomize-answers")
        default_points_input = self.shadow_driver.find_element("#qed-points")
        grading_method_container = Select(self.shadow_driver.find_element("#qed-grading-type-selector"))
        save_btn = self.shadow_driver.find_element(".primary[name=\"Submit\"]")
        
        # Fill in M-S form
        question_text_input.click()
        question_text_input.send_keys(question_text)

        for i in range(len(options_text)):
            self.driver.execute_script("arguments[0].scrollIntoView();", option_text_inputs[i]) 
            option_text_inputs[i].click()
            option_text_inputs[i].send_keys(options_text[i])
           
        for answer in correct_answers:
            answer_checkboxes[answer - 1].click()
        
        self.driver.execute_script("arguments[0].scrollIntoView();", randomize_checkbox)    
        if randomize == True:
            randomize_checkbox.click()
        
        self.driver.execute_script("arguments[0].scrollIntoView();", save_btn)    
        if grading_method == "right answers":
            grading_method_container.select_by_index(1)
        elif grading_method == "right answers limited selection":
            grading_method_container.select_by_index(2)
        elif grading_method == "right minus wrong":
            grading_method_container.select_by_index(3)
        else:
            grading_method_container.select_by_index(0)
    
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        save_btn.click()
        self.reset_frame()
    
    def written_answer(self, question_data):
        self.switch_frame()

        print(f"From written_answer, received data dict: {question_data}")

        # Data extraction
        # Text
        question_text = question_data["Question Text"]
        # Numbers
        points = int(question_data["Points"])

        # Web components declarations
        # Web element declarations
        question_text_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Question Text\"]")
        default_points_input = self.shadow_driver.find_element("#qed-points")
        save_btn = self.shadow_driver.find_element(".primary[name=\"Submit\"]")

        # Fill in WR form
        question_text_input.click()
        question_text_input.send_keys(question_text)

        self.driver.execute_script("arguments[0].scrollIntoView();", save_btn)
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        save_btn.click()
        self.reset_frame()
    
    def short_answer(self, question_data):
        self.switch_frame()

        print(f"From short_answer, received data dict: {question_data}")

        # Data extraction
        # Numbers
        num_text_fields = int(question_data["Number of Text Fields"])
        points = int(question_data["Points"])
        # Text
        question_text = question_data["Question Text"]
        grading_method = None
        if num_text_fields >= 2:
            grading_method = question_data["Grading Method"].lower()
        # List  
        correct_answers = parse_csv_round_braces(question_data["Correct Answer"])

        # Add enough blanks to match num_text_fields
        add_blank_btn = self.shadow_driver.find_element("#add-blank")
        for i in range(num_text_fields - 1):
            add_blank_btn.click()
            sleep(1)

        # Web elements declarations
        question_text_input = self.shadow_driver.find_element(".qed-d2l-htmleditor-container[label^=\"Question Text\"]")
        answer_inputs = self.shadow_driver.find_elements(".qed-tagfield-input")
        default_points_input = self.shadow_driver.find_element("#qed-points")
        grading_method_container = Select(self.shadow_driver.find_element("#qed-grading-type-selector"))
        save_btn = self.shadow_driver.find_element(".primary[name=\"Submit\"]")

        # Fill in WR form
        question_text_input.click()
        question_text_input.send_keys(question_text)

        for i in range(num_text_fields):
            self.driver.execute_script("arguments[0].scrollIntoView();", answer_inputs[i])    
            answer_inputs[i].click()
            answer_inputs[i].send_keys(correct_answers[i])

        self.driver.execute_script("arguments[0].scrollIntoView();", default_points_input)    
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        self.driver.execute_script("arguments[0].scrollIntoView();", save_btn)    
        if grading_method == "all or nothing":
            grading_method_container.select_by_index(1)
        else:
            grading_method_container.select_by_index(0)

        save_btn.click()
        self.reset_frame()
    
    def matching(self, question_data):
        # self.switch_frame()
        focus_on_library_homepage(self.driver)

        print(f"From matching, received data dict: {question_data}")

        # Data extraction
        # Text
        question_title = question_data["Title"]
        question_text = question_data["Question Text"]
        grading_method = question_data["Grading Method"].lower()
        # Numbers
        points = int(question_data["Points"])
        num_pairs = int(question_data["Number of Pairs"])
        # List
        options_text = parse_csv_round_braces(question_data["Options Text"])
        matching_text = parse_csv_round_braces(question_data["Correct Answer"])

        # Remove all options/matches except for 1 each
        remove_choice_btns = self.shadow_driver.find_elements("a[title^=\"Remove Option\"]")
        print(f"Remove Choices: {len(remove_choice_btns)}")
        self.driver.execute_script("arguments[0].scrollIntoView();", remove_choice_btns[1])
        remove_choice_btns[1].click()
        sleep(2)
        remove_match_btns = self.shadow_driver.find_elements("a[title^=\"Remove match\"]")
        print(f"Remove Matches: {len(remove_match_btns)}")
        self.driver.execute_script("arguments[0].scrollIntoView();", remove_match_btns[1])
        remove_match_btns[1].click()
        sleep(2)

        # Add options/matches to match with num_pairs
        for i in range(num_pairs - 1):
            add_choice_btn = self.shadow_driver.find_element("a[title=\"Add Choice\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_choice_btn)
            add_choice_btn.click()
            sleep(2)
            add_match_btn = self.shadow_driver.find_element("a[title=\"Add Match\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_match_btn)
            add_match_btn.click()
            sleep(2)

        # Web elements declarations
        question_title_input = self.shadow_driver.find_element("#z_o")
        default_points_input = self.shadow_driver.find_element("input[aria-label=\"Points\"]")
        question_text_input = self.shadow_driver.find_element(".d2l-htmleditor-wc[label=\"Question Text\"]")
        grading_method_choices = self.shadow_driver.find_elements(".d2l-radio-inline")

        option_matches_text_inputs = self.shadow_driver.find_elements(".d2l-htmleditor-wc[label^=\"Edit Entry\"]")
        halfway_index = len(option_matches_text_inputs) // 2
        option_text_inputs = option_matches_text_inputs[:halfway_index]
        match_text_inputs = option_matches_text_inputs[halfway_index:]

        print(f"Option inputs: {len(option_text_inputs)}")
        print(f"Matches inputs: {len(match_text_inputs)}")

        save_btns = self.shadow_driver.find_elements("button.d2l-button")

        # Fill in MAT form
        question_title_input.click()
        question_title_input.send_keys(question_title)

        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        question_text_input.click()
        question_text_input.send_keys(question_text)

        self.driver.execute_script("arguments[0].scrollIntoView();", grading_method_choices[0])    
        if grading_method == "all or nothing":
            grading_method_choices[1].click()
        elif grading_method == "right minus wrong":
            grading_method_choices[2].click()
        else:
            grading_method_choices[0].click()
        
        for i in range(num_pairs):
            self.driver.execute_script("arguments[0].scrollIntoView();", option_text_inputs[i])    
            option_text_inputs[i].click()
            option_text_inputs[i].send_keys(options_text[i])
        
        for i in range(num_pairs):
            self.driver.execute_script("arguments[0].scrollIntoView();", match_text_inputs[i])    
            match_text_inputs[i].click()
            match_text_inputs[i].send_keys(matching_text[i])

        click_element_of_elements(save_btns, "Save", "text")
        self.reset_frame()

    def fill_in_the_blanks(self, question_data):
        focus_on_library_homepage(self.driver)

        print(f"From fill_in_the_blanks, received data dict: {question_data}")

        # Data extraction
        # Text
        question_title = question_data["Title"]
        # Numbers
        points = int(question_data["Points"])
        # List
        correct_answers = parse_csv_round_braces(question_data["Correct Answer"])
        question_text = question_data["Question Text"].split("_")
        
        # Remove the last text area so there's 1 textarea and 1 blank
        remove_text_btns = self.shadow_driver.find_elements("a[title^=\"Remove text\"]")
        self.driver.execute_script("arguments[0].scrollIntoView();", remove_text_btns[1])
        remove_text_btns[1].click()
        sleep(2)

        # Add blanks and texts as necessary to match the question text
        for i in range(1, len(question_text) - 1):
            add_text_btn = self.shadow_driver.find_element("a[title^=\"Add text\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_text_btn)
            add_text_btn.click()
            sleep(2)
            add_blank_btn = self.shadow_driver.find_element("a[title^=\"Add blanks\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_blank_btn)
            add_blank_btn.click()
            sleep(2)

        add_text_btn = self.shadow_driver.find_element("a[title^=\"Add text\"]")
        self.driver.execute_script("arguments[0].scrollIntoView();", add_text_btn)
        add_text_btn.click()
        sleep(2)

        # Web component declarations
        question_title_input = self.shadow_driver.find_element("#z_o")
        default_points_input = self.shadow_driver.find_element("input[aria-label^=\"Points\"]")
        text_area_inputs = self.shadow_driver.find_elements(".d2l-htmleditor-wc[label^=\"<strong>Text\"]")
        # question_text_input = self.shadow_driver.find_element(".d2l-htmleditor-wc[label^=\"Question Text\"]")
        blank_text_inputs = self.shadow_driver.find_elements("input[title^=\"Answer\"]")
        percent_weight = 100 / question_data["Question Text"].count("_")
        blank_weight_inputs = self.shadow_driver.find_elements("input[aria-label^=\"Edit weighted percent\"]")
        save_btns = self.shadow_driver.find_elements(".d2l-button")

        # Fill in FIB form
        question_title_input.click()
        question_title_input.send_keys(question_title)

        self.driver.execute_script("arguments[0].scrollIntoView();", default_points_input)    
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)
        
        # Fill in the answers
        for (i, blank) in enumerate(blank_text_inputs):
            self.driver.execute_script("arguments[0].scrollIntoView();", blank)
            blank.click()
            blank.send_keys(correct_answers[i])

        # Set all blanks to be weighted as 100%
        for blank in blank_weight_inputs:
            self.driver.execute_script("arguments[0].scrollIntoView();", blank)
            blank.click()
            self.driver.execute_script("arguments[0].value = ''", blank)
            blank.send_keys(str(percent_weight))

        # # PROBLEM: SELENIUM SAYS THIS ELEMENT IS NOT INTERACTABLE
        # # Fill in the text areas
        # for (i, textarea) in enumerate(text_area_inputs):
        #     self.driver.execute_script("arguments[0].scrollIntoView();", textarea)
        #     sleep(5)
        #     textarea.click()
        #     sleep(2)
        #     textarea.send_keys(question_text[i])

        click_element_of_elements(save_btns, "Save", "text")
        self.reset_frame()

    def ordered(self, question_data):
        focus_on_library_homepage(self.driver)
        print(f"From ordered, received data dict: {question_data}")

        # Data extraction
        # Text
        question_title = question_data["Title"]
        question_text = question_data["Question Text"]
        grading_method = question_data["Grading Method"].lower()
        # Numbers
        points = int(question_data["Points"])
        num_options = int(question_data["Number of Options"])
        # Lists
        options_text = parse_csv_round_braces(question_data["Options Text"])
        feedback_text = parse_csv_round_braces(question_data["Feedback on Options"])

        # Remove all options except for the last one
        for i in range(num_options - 1):
            remove_option_btns = self.shadow_driver.find_elements("a[title^=\"Remove Entry\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", remove_option_btns[-1])
            
            remove_option_btns[-1].click()
            sleep(2)

        # Add options until matching num_options
        for i in range(num_options - 1):
            add_option_btn = self.shadow_driver.find_element("a[title=\"Add Item\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_option_btn)
            add_option_btn.click()
            sleep(2)

        # Web element declarations
        question_title_input = self.shadow_driver.find_element("#z_o")
        default_points_input = self.shadow_driver.find_element("input[aria-label=\"Points\"]")
        question_text_input = self.shadow_driver.find_element(".d2l-htmleditor-wc[label=\"Question Text\"]")
        grading_method_choices = self.shadow_driver.find_elements(".d2l-radio-inline")
        option_text_inputs = self.shadow_driver.find_elements(".d2l-htmleditor-wc[label$=\"Value\"]")
        feedback_text_inputs = self.shadow_driver.find_elements(".d2l-htmleditor-wc[label$=\"Feedback\"]")
        save_btns = self.shadow_driver.find_elements(".d2l-button")

        # Fill in ORD form
        question_title_input.click()
        question_title_input.send_keys(question_title)

        self.driver.execute_script("arguments[0].scrollIntoView();", default_points_input)    
        default_points_input.click()
        # Clear the default points field
        self.driver.execute_script("arguments[0].value = ''", default_points_input)
        default_points_input.send_keys(points)

        question_text_input.click()
        question_text_input.send_keys(question_text)

        self.driver.execute_script("arguments[0].scrollIntoView();", grading_method_choices[0])    
        if grading_method == "equally weighted":
            grading_method_choices[0].click()
        elif grading_method == "right minus wrong":
            grading_method_choices[2].click()
        else:
            grading_method_choices[1].click()
        
        for (i, option) in enumerate(option_text_inputs):
            self.driver.execute_script("arguments[0].scrollIntoView();", option)
            option.click()
            option.send_keys(options_text[i])
        
        print(f"Length of feedback_text_inputs: {len(feedback_text_inputs)}")
        feedback_text_inputs = feedback_text_inputs[0:-1]
        for (i, feedback) in enumerate(feedback_text_inputs):
            self.driver.execute_script("arguments[0].scrollIntoView();", feedback)
            feedback.click()
            feedback.send_keys(feedback_text[i])

        click_element_of_elements(save_btns, "Save", "text")
        self.reset_frame()

    def likert(self, question_data):
        focus_on_library_homepage(self.driver)
        print(f"From likert, received data dict: {question_data}")

        # Data extraction 
        # Text
        question_text = question_data["Question Text"]
        question_title = question_data["Title"]
        scale_type = question_data["Scale Type"].lower()
        # Numbers
        num_options = int(question_data["Number of Options"])
        # Boolean
        enable_na = lambda choice : bool(choice == "yes")
        enable_na = enable_na(question_data["Enable N/A Option"].lower())
        # Lists
        options_text = parse_csv_round_braces(question_data["Options Text"])

        # Remove the last option so that only one remains
        remove_option_btns = self.shadow_driver.find_elements("a[title^=\"Remove Entry\"]")
        self.driver.execute_script("arguments[0].scrollIntoView();", remove_option_btns[-1])
        remove_option_btns[-1].click()
        sleep(2)

        # Add options until matching num_options
        for i in range(num_options - 1):
            add_option_btn = self.shadow_driver.find_element("a[title=\"Add Option\"]")
            self.driver.execute_script("arguments[0].scrollIntoView();", add_option_btn)
            add_option_btn.click()
            sleep(2)

        # Web element declarations
        questions_title_input = self.shadow_driver.find_element("#z_o")
        questions_text_input = self.shadow_driver.find_element(".d2l-htmleditor-wc[label=\"Introductory Text\"]")
        scale_choices = self.shadow_driver.find_elements(".d2l-radio-inline")
        enable_na_checkbox = self.shadow_driver.find_element("#z_bl")
        option_text_inputs = self.shadow_driver.find_elements(".d2l-htmleditor-wc[label$=\"Value\"]")
        save_btns = self.shadow_driver.find_elements(".d2l-button")

        # Fill in LIK form
        questions_title_input.click()
        questions_title_input.send_keys(question_title)

        questions_text_input.click()
        questions_text_input.send_keys(question_text)

        self.driver.execute_script("arguments[0].scrollIntoView();", scale_choices[0])    
        if scale_type == "one to five":
            scale_choices[0].click()
        elif scale_type == "one to eight":
            scale_choices[1].click()
        elif scale_type == "one to ten":
            scale_choices[2].click()
        elif scale_type == "agreement":
            scale_choices[3].click()
        elif scale_type == "satisfaction":
            scale_choices[4].click()
        elif scale_type == "frequency":
            scale_choices[5].click()
        elif scale_type == "importance":
            scale_choices[6].click()
        elif scale_type == "opposition":
            scale_choices[7].click()

        if enable_na == True:
            self.driver.execute_script("arguments[0].scrollIntoView();", enable_na_checkbox)
            enable_na_checkbox.click()

        for (i, option) in enumerate(option_text_inputs):
            self.driver.execute_script("arguments[0].scrollIntoView();", option)    
            option.click()
            option.send_keys(options_text[i])
            
        click_element_of_elements(save_btns, "Save", "text")
        self.reset_frame()
    
    def navigate_to_question_form(self, question_type):
        wait_until_page_fully_loaded(self.driver, 10)
        self.reset_frame()
        focus_on_library_homepage(self.driver)
        sleep(1)

        # Click on "New" button
        action_btns = self.shadow_driver.find_elements(".d2l-buttonmenu-text")
        print("From new_question")
        click_element_of_elements(action_btns, "New")

        sleep(1)

        # Click on new question button based on question type to get to the section form
        new_question_btns = self.shadow_driver.find_elements(".d2l-menu-item-text")
        for btn in new_question_btns:
            if btn.text != "":
                if btn.text.split(" ")[-1] == "(" + question_type + ")" and btn.text.split(" ")[-1] != "(" + "FIB" + ")":
                    # self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.shadow_driver.get_parent_element(btn))
                    btn.click()
                    break
        
        wait_until_page_fully_loaded(self.driver, 10)
        sleep(3)
        self.reset_frame()

    # Creates a single quiz question from start to finish
    def new_question(self, question_type, question_data):
        self.navigate_to_question_form(question_type)

        # Call the appropriate function to fill the question form
        if question_type == "T/F":
            self.true_false(question_data)
        elif question_type == "MC":
            self.multiple_choice(question_data)
        elif question_type == "M-S":
            self.multi_select(question_data)
        elif question_type == "WR":
            self.written_answer(question_data)
        elif question_type == "SA":
            self.short_answer(question_data)
        elif question_type == "MAT":
            self.matching(question_data)
        # elif question_type == "FIB":
        #     self.fill_in_the_blanks(question_data)
        elif question_type == "ORD":
            self.ordered(question_data)
        elif question_type == "LIK":
            self.likert(question_data)
        else:
            print("From new_question in Question_maker: No such question type was found!")