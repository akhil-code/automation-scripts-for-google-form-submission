from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import random
import time

class Form:
    __instance__ = None

    def __init__(self):
        self.url = 'https://goo.gl/forms/wNAmuCXUceETOh1r1'
        # radio button
        self.question_holder_css_selector = 'content[role=presentation]'
        self.radio_button_class_name = 'exportOuterCircle'
        # submit button
        self.submit_button_class_name = 'quantumWizButtonPaperbuttonLabel'
        
        if Form.__instance__ == None:
            Form.__instance__ = self


    def get_instance():
        if Form.__instance__ == None:
            Form()
        return Form.__instance__

def initialize():
    target_form = Form.get_instance()
    driver = webdriver.Firefox()
    driver.get(target_form.url)
    return driver

def assert_correct_page(driver):
    assert "Untitled form" in driver.title

def fill_username(driver, name):
    name_input = driver.find_element_by_tag_name('input')
    name_input.send_keys(name)

def fill_options(driver):
    target_form = Form.get_instance()
    css_selector_holder = target_form.question_holder_css_selector
    button_class_name = target_form.radio_button_class_name

    content_holders = driver.find_elements_by_css_selector(css_selector_holder)
    for holder in content_holders:
        buttons = holder.find_elements_by_class_name(button_class_name)
        random.choice(buttons).click()


def click_submit(driver):
    # class_name = 'quantumWizButtonPaperbuttonLabel'
    class_name = Form.get_instance().submit_button_class_name
    
    button = driver.find_element_by_class_name(class_name)
    button.click()

def read_names_from_file():
    names = []
    with open('names.csv') as f:
        names = [row.split(',')[0] for row in f]
    return names

def fill_form(driver, name):
    fill_username(driver, name)
    fill_options(driver)
    click_submit(driver)

def open_new_form(driver):
    target_form = Form.get_instance()
    driver.get(target_form.url)

def main():
    driver = initialize()
    names = read_names_from_file()

    assert_correct_page(driver)

    for i in range(10000):
        try:
            name = random.choice(names)
            fill_form(driver, name)
            print(f'finished form {i} -> {name}')
            time.sleep(2)
            open_new_form(driver)
        except:
            print(f'unable to print form {i}')

if __name__ == '__main__':
    main()
