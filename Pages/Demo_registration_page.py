import allure
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Base import selenium_cmd_helpers
from Utilities.Utils import custom_log, data_base_validation


class demo_registration_page:
    def __init__(self,driver):
        self.driver = driver
        self.shadow_root = self.driver.find_element(By.ID, 'registration-app').shadow_root

    def input_first_name(self,first_name_value):
        try:
            # enter the first_name
            first_name_js_element = self.shadow_root.find_element(By.ID,"first_name")
            selenium_cmd_helpers.javascript_executor(self.driver,first_name_js_element,'click')
            first_name_js_element.send_keys(first_name_value)
            custom_log().info(f"The first name entered : {first_name_value}" )
        except Exception as e:
            custom_log().error(f"Unable to enter the first name due to the following error - {e}")
            raise e

    def input_middle_name(self,skip_name,middle_name_value):
         try:
            if skip_name.lower()=='n':
                # skip the middle name checkbox
                middle_name_checkbox_js_element = self.shadow_root.find_element(By.ID, 'skip_middle_name')
                selenium_cmd_helpers.javascript_executor(self.driver, middle_name_checkbox_js_element, 'click')
                custom_log().info("The middle name checkbox is skipped")
            else :
                middle_name_checkbox_js_element = self.shadow_root.find_element(By.ID, 'middle_name')
                selenium_cmd_helpers.javascript_executor(self.driver, middle_name_checkbox_js_element, 'click')
                middle_name_checkbox_js_element.send_keys(middle_name_value)
                custom_log().info(f"The middle name entered: {middle_name_value}" )
         except Exception as e:
             if skip_name.lower()=='n':
                 custom_log().error(f"Unable to skip the middle name due to the following error - {e}")
                 raise e
             else :
                 custom_log().error(f"Unable to input the middle name due to the following error - {e}")
                 raise e




    def input_last_name(self,last_name_value):
        try:
            last_name_js_element = self.shadow_root.find_element(By.ID, "last_name")
            selenium_cmd_helpers.javascript_executor( self.driver, last_name_js_element,'click')
            last_name_js_element.send_keys(last_name_value)
            custom_log().info(f"The last name entered is: {last_name_value}" )
        except NoSuchElementException as e:
            custom_log().error(f"Unable to enter the last name due to the following error - {e}")
            raise e

    def input_email(self,email_value):
        try:
            #scroll to email field and enter the email id
            email_js_element = self.shadow_root.find_element(By.ID,"email")
            selenium_cmd_helpers.javascript_executor( self.driver, email_js_element,'click')
            email_js_element.send_keys(email_value)
            custom_log().info(f"The email entered is: {email_value}" )
        except Exception as e:
            custom_log().log.error(f"Unable to enter the email due to the following error - {e}")
            raise e

    def input_phone(self,phone_number_value):
        try:

            #enter the phone number
            phone_js_element = self.shadow_root.find_element(By.ID,"phone")
            selenium_cmd_helpers.javascript_executor( self.driver, phone_js_element, 'click')
            phone_js_element.send_keys(phone_number_value)
            custom_log().info(f"The phone entered is: {phone_number_value}" )
        except Exception as e:
            custom_log().error(f"Unable to enter the phone number due to the following error - {e}")
            raise e

    def click_submit_button(self,browser_name):
        try :
            #take screenshot before submitting the form
            with allure.step("Take screenshot before submitting the form"):
                selenium_cmd_helpers.take_screenshot(self.driver,"demo_acc_creation",browser_name)
                #click the submit button
                submit_button_js_element = self.shadow_root.find_element(By.CSS_SELECTOR,"button[type='Submit']")
                selenium_cmd_helpers.javascript_executor( self.driver, submit_button_js_element, 'click')
                #wait for the form to submit the form
                submit_pop_up_modal=self.driver.find_element(By.CLASS_NAME,"ReactModalPortal")
                if submit_pop_up_modal:
                    selenium_cmd_helpers.explicit_wait(self.driver,"ReactModal__Content ReactModal__Content--after-open","presence_of_element_located","class")


            # take screenshot before submitting the form
            with allure.step("Take screenshot after submitting the form"):
               selenium_cmd_helpers.take_screenshot(self.driver, "demo_acc_creation", browser_name)
               custom_log().info("Submit button is clicked")

        except Exception as e:
            custom_log().error(f"Unable to click on submit button due to the error - {e}")
            raise e


    def customer_verification(self,email_value,test_environment):
        sql_query= (f"select cust_type.name as customer_type,cust.id,cust.name,cust.email,cust.branch_id,br.name as branch_name "
                    f"from tb_customer cust "
                    f"inner join tb_branch br on cust.branch_id=br.id"
                    f"inner join tb_customer_type cus_type on cust.type_id=cus_type.id "                    
                    f"where email={email_value} ")
        try:
            custom_log().info("Sending the information to db to ensure the registration is successful")
            result=data_base_validation(sql_query,test_environment)
            if result:
                custom_log().info("customer registered successfully")
            else:
                custom_log().error("Cannot validate customer")
            return result

        except Exception as e:
            custom_log().error(f"unable to fetch data from DB due to error - {e}")
            raise e



