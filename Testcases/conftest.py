import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from Base import selenium_cmd_helpers
from Utilities.Utils import custom_log
from configfiles.Read_user_inputs import read_test_data
import chrome_version


@pytest.fixture(scope="class")
def read_user_input():
    try:
        user_inputs = read_test_data()
        url, first_name_value, middle_name_value, last_name_value, email_value, phone_number_value, au_demo_web_page_title,test_environment = user_inputs
        if len(user_inputs) < 8:
           fail_with_log("Insufficient data in test data file")
        return {
            "url": url,
            "first_name": first_name_value,
            "middle_name": middle_name_value,
            "last_name": last_name_value,
            "email": email_value,
            "phone_number": phone_number_value,
            "page_title": au_demo_web_page_title,
            "test_environment":test_environment
        }
    except Exception as ex:
        custom_log().error("unable to read data - " + str(ex))
        pytest.fail("Failed to read user input")


@pytest.fixture(params=["chrome"],scope="class",autouse=True)
def setup(request,read_user_input):
    web_driver = None
    try:
        url = read_user_input["url"]
        page_title = read_user_input["page_title"]
        # Initialize WebDriver based on browser_name
        with allure.step(f"Initialize WebDriver based on browser_name {request.param}"):
            if request.param == 'chrome':
                chrome_latest_version=chrome_version.get_chrome_version()
                web_driver  = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_latest_version).install()))
            elif request.param == 'firefox':
                web_driver =webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            elif request.param == 'edge':
                web_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            else:
                fail_with_log(f"Unsupported browser: {request.param}")
            custom_log().info(f"Opened the {request.param}  browser")


        # Assign driver to test class
        request.cls.driver = web_driver
        yield web_driver,read_user_input,request.param,url,page_title

    except Exception as error:
        custom_log().error(f'Unable to launch the browser {request.param} due to error: {error}')

    finally:
        #  Ensure the WebDriver is quit after the test runs if it was created
        if webdriver:
            web_driver.quit()

# Hook to capture test results and quit the WebDriver if the test failed
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # Check if the failure was due to pytest.fail
        if getattr(call.excinfo.value, pytest.fail.Exception):
            failure_message = str(call.excinfo.value)
            custom_log().error(f"Test {item.name} failed with message: {failure_message}")
        else:
            custom_log().error(f"Test {item.name} failed. Error: {call.excinfo.value}")

        # Get the WebDriver instance from the test class fixture
        driver = item.cls.driver if hasattr(item.cls, 'driver') else None
        if driver:
            custom_log().error(f"Test {item.name} failed. Quitting WebDriver...")
            driver.quit()

def fail_with_log(message):
    """
    Custom wrapper to log the message before raising pytest.fail
    """
    custom_log().error(f"Test failed with message: {message}")
    pytest.fail(message)