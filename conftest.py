#!/usr/bin/python3
# -*- encoding=utf8 -*-

# This is example shows how we can manage failed tests
# and make screenshots after any failed test case.

import pytest
import allure
import uuid


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')

    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_make_report(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):
    browser = selenium
    browser.set_window_size(1280, 768)

    # Return browser instance to a test case:
    yield browser

    # Do tear down (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screenshot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screenshot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) +
                                    '.png')

            # Attach screenshot to an Allure report:
            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here


def get_test_case_docstring(item):
    """ 
    This function gets doc string from a test case and formats it
    to show this docstring instead of the test case name in reports.
    """

    full_name = ''

    if item._obj.__doc__:
        # Remove extra space from the doc string:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            res_keys = sorted([k for k in params])
            # Create List based on Dict:
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Add dict with all parameters to the name of test case:
            full_name += ' Parameters ' + str(', '.join(res))
            full_name = full_name.replace(':', '')

    return full_name


def pytest_item_collected(item):
    """ 
    This function modifies the names of test cases "on the fly"
    during the execution of test cases.
    """

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)


def pytest_collection_finish(session):
    """ 
    This function modified names of test cases "on the fly"
    when we are using --collect-only parameter for pytest
    (to get the full list of all existing test cases).
    """

    if session.config.option.collectonly is True:
        for item in session.items:
            # If a test case has a doc string, we need to modify its name to
            # its doc string to show human-readable reports and to
            # automatically import test cases to a test management system.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)

        pytest.exit('Done!')
