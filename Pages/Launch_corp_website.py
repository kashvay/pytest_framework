import allure

from Base import selenium_cmd_helpers
from Utilities.Utils import custom_log


class launch_application:
    def __init__(self,driver):
        self.driver = driver

    def open_corporate_application(self,browser_name,url,page_title):
        try:
            # Navigate to URL and validate page title
            with allure.step(f"Navigate to URL {url} and validate page title"):
                custom_log().info("Open the URL")
                self.driver.get(url)
                custom_log().info(f"Launching website: {url} using {browser_name.capitalize()} browser.")
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                title = self.driver.title
                if title != page_title:
                    selenium_cmd_helpers.take_screenshot(self.driver, "initial_setup", browser_name)
                    raise Exception(f"Page title mismatch. Expected: '{page_title}', but got: '{title}'")
                selenium_cmd_helpers.take_screenshot(self.driver, "initial_setup", browser_name)
        except Exception as error:
            custom_log().error(f'Unable the launch the application due to the following error: {error}')


