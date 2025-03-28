import json
import os
import random

from Utilities import Utils
from Utilities.Utils import custom_log


def generate_email(base_email):
    # Split the base email at '@' to get the part before the '@' (username) and after (domain)
    username, domain = base_email.split('@')
    # Assign the number using randint function
    number = str(random.randint(10, 999999))
    # Append the number to the username part
    new_username = f"{username}+{number}"
    # Combine the new username with the domain
    new_email = f"{new_username}@{domain}"

    return new_email

def read_test_data():
    test_environment = None
    url = None
    first_name = None
    middle_name = None
    last_name = None
    email = None
    phone_number = None
   # browser_name = None
    au_demo_web_page_title = None

    try:
        # open the data config file in the mentioned location
        file_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "dataconfig.json"))
        with open(file_path,'r') as file:
            jsonobj = json.load(file)
        # loop through thw JSON file for all settings and assign to local variable.
        for i in jsonobj:
            if i == "environment":
                test_environment = str(jsonobj[i])
                custom_log().info("The test environment for this test run is : " + test_environment)

            elif i == 'app_details':
                for app_details in jsonobj["app_details"]:
                    if test_environment == "staging":
                        url = str(app_details["demo_app_url_test"])
                    else:
                        url = str(app_details["demo_app_url_prod"])

            elif i == 'registration_form_inputs':
                for reg_dtl in jsonobj["registration_form_inputs"]:
                    first_name = str(reg_dtl["first_name"])
                    middle_name = str(reg_dtl["middle_name"])
                    last_name = str(reg_dtl["last_name"])
                    email = generate_email(str(reg_dtl["email"]))
                    phone_number = str(reg_dtl["phone"])

            #elif i == 'browser_name':
            #    browser_name = str(jsonobj[i])

            elif i =='au_demo_web_page_title':
                au_demo_web_page_title=str(jsonobj[i])

        custom_log().info("The test data fetched successfully")

    except Exception as e:
        custom_log().info("Unable to fetch the test data due to   " + str(e))

    # return all the assigned variable
    return url, first_name, middle_name, last_name, email, phone_number,au_demo_web_page_title,test_environment


class Read_user_inputs:
    def __init__(self):
     self.log =Utils.custom_log()




