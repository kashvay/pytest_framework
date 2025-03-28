import datetime
import os

import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.Utils import custom_log


def select_dropdown(select_type, find_element_value, text, driver):
    try:
        element = driver.find_element_by_xpath(find_element_value)
        select_element = select.Select(element)
        if select_type == 'value':
            select_element.select_by_value(text)
        else:
            select_element.select_by_index(text)
    except select_dropdown as e:
        custom_log().error('Unable to select dropdown' + str(e))



def javascript_executor(driver, element, jstype):
    try:
        web_element= element
        if jstype.lower() == 'click':
            driver.execute_script("arguments[0].click();", web_element)
        elif jstype.lower() == 'scroll':
            driver.execute_script("arguments[0].scrollIntoView();", web_element)
    except javascript_executor as e:
        custom_log().error('JavaScript executor failed'+ str(e))

def explicit_wait(driver, element,wait_type,locator_type,text=None):
    try:
        web_element = element
        wait = WebDriverWait(driver, 20)
        if wait_type.lower()=='clickable':
            if locator_type.lower()=='id':
                wait.until(EC.element_to_be_clickable(driver.find_element(By.ID,"element")))
            elif locator_type.lower()== 'class':
                wait.until(EC.element_to_be_clickable(driver.find_element(By.CLASS_NAME, "element")))
            elif locator_type.lower()=='css_selector':
                wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "element")))
                wait.until(EC.visibility_of_all_elements_located())

        elif wait_type.lower()=='text_to_be_present':
            if locator_type.lower()=='id':
                wait.until(EC.text_to_be_present_in_element((By.ID,"element"),text))
            elif locator_type.lower()== 'class':
                wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "element"),text))
            elif locator_type.lower()=='css_selector':
                wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "element"),text))

        elif wait_type.lower()=='presence_of_element_located':
            if locator_type.lower()=='id':
                wait.until(EC.presence_of_element_located((By.ID,"element")))
            elif locator_type.lower()== 'class':
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "element")))
            elif locator_type.lower()=='css_selector':
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "element")))

    except TimeoutException as e:
        if wait_type.lower() == 'clickable':
            custom_log().error('Timeout while waiting for element to be clicked ' + str(e))
        elif wait_type.lower()=='text_to_be_present':
            custom_log().error('Timeout while waiting for the text to be present ' + str(e))
        elif wait_type.lower()=='visibility_of_element':
            custom_log().error('Timeout while waiting for element to be visible ' + str(e))

def get_shadow_root(driver, locator_data):
    shadow_root=None
    try:
        shadow_root=driver.find_element(By.ID, locator_data).shadow_root
    except NoSuchElementException as e:
        custom_log().error('Shadow root element not found'+ str(e))
    return shadow_root

def take_screenshot(driver,test_name,browser_name):
    try:
        # Get the current timestamp for the image name
        today = datetime.datetime.now()
        image_name = today.strftime("%d-%m-%Y %H:%M:%S").replace(" ", "_").replace(":",
                                                                                   "-")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        screenshot_dir = os.path.join(project_root,"Screenshots")
        screenshot_name= f"{test_name}_{browser_name}_{image_name}.png"

        # Use JavaScript to get the full width and height of the webpage
        width = driver.execute_script(
            "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );")
        height = driver.execute_script(
            "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

        # Set the window size to match the entire webpage
        driver.set_window_size(width, height)

        # Capture and attach screenshot to Allure without saving to disk
        allure.attach(
            driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        custom_log().info(f"Screenshot named {screenshot_name } saved to allure report")
    except NoSuchElementException as e:
        custom_log().info(f'Screenshot not taken due to error: {str(e)}')
    except Exception as e:
        custom_log().info(f"An error occurred while taking the screenshot: {str(e)}")

class Selenium_Cmd_Helpers:

    def __init__(self, driver):
        self.driver = driver




