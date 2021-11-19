from selenium.webdriver.support.ui import WebDriverWait

# Helper function to click an element given 
# a collection of elements
def click_element_of_elements(elements, innertext):
    if not elements[0].text == "":
        for el in elements:
            if el.text == innertext:
                el.click()
                break
    else:
        for el in elements:
            if el.get_attribute('text') == innertext:
                el.click()
                break

# Executes some JS to ensure that the HTML is fully rendered before any automated interactions
def wait_until_page_fully_loaded(driver, wait_time):
    WebDriverWait(driver, wait_time).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

# For debugging purposes, prints the length and contents of a collection of elements
def about(elements, var_name):
    print(f"{var_name}: {elements}")
    print(f"{var_name} length: {len(elements)}")
    for (i, el) in enumerate(elements):
        if not el.text == "":
            print(f"Element {i + 1} text: {el.text}")
        else:
            print(f"Element {i + 1} text: {el.get_attribute('text')}")