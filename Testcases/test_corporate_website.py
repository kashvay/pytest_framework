from datetime import datetime

import allure
import pytest

from Base import selenium_cmd_helpers
from Pages.Demo_registration_page import demo_registration_page
from Pages.Launch_corp_website import launch_application
from Utilities.Utils import custom_log



@pytest.mark.usefixtures("setup")
class BasicTest:
    pass

@allure.feature("Registration")
@allure.story("Demo account registration")
@allure.severity(allure.severity_level.CRITICAL)
class Testcorporate_website(BasicTest):


    def setup_method(self):
      self.driver = self.driver
     # self.log=Utils.custom_log()

    @pytest.fixture(scope="session")
    def test_run_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @pytest.mark.smoke_test
    def test_corporate_site (self,setup,test_run_date):
        try:
            _, _, browser_name,url,page_title = setup
            allure.attach(test_run_date, name="Test Run Date", attachment_type=allure.attachment_type.TEXT)
            launch_application(self.driver).open_corporate_application(browser_name,url,page_title)
        except Exception as error:
            custom_log().error("Unable to launch the application")
            raise error

    @pytest.mark.regression
    def test_create_demo_account(self,setup,test_run_date):
        try:
            _, _, browser_name,url,page_title = setup
            user_input_dict=setup[1]
            first_name_value = user_input_dict["first_name"]
            middle_name_value=user_input_dict["middle_name"]
            last_name_value=user_input_dict["last_name"]
            email_value=user_input_dict["email"]
            phone_number_value=user_input_dict["phone_number"]
            test_environment=user_input_dict["test_environment"]

            allure.attach(test_run_date, name="Test Run Date", attachment_type=allure.attachment_type.TEXT)

            # launch the corporate application
            with allure.step("Launch the browser and open the application"):
                launch_application(self.driver).open_corporate_application(browser_name, url, page_title)

            # enter the first name
            with allure.step("input first name"):
                demo_registration_page(self.driver).input_first_name(first_name_value)

            # skip the middle name checkbox
            with allure.step("input middle name"):
                demo_registration_page(self.driver).input_middle_name('N', middle_name_value)

            # enter the last name
            with allure.step("input last name"):
                demo_registration_page(self.driver).input_last_name(last_name_value)

            # enter the email id
            with allure.step("input email"):
                demo_registration_page(self.driver).input_email(email_value)

            # enter the phone number
            with allure.step("input phone number"):
                demo_registration_page(self.driver).input_phone(phone_number_value)

            # click the submit button
            with allure.step("click on submit button"):
                demo_registration_page(self.driver).click_submit_button(browser_name)

            with allure.step("validate the registration"):
                demo_registration_page(self.driver).customer_verification(email_value,test_environment)

            custom_log().info("The demo account registration is completed")

        except Exception as error:
            custom_log().error(f"Unable to proceed with the application due to the error- {error}")
            raise error


