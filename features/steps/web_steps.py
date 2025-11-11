from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    if element_name == "Product ID":
        element_id = "product_id"
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)
    
@when('I change the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}"')
def step_impl(context, text, element_name):
    element_id = 'search_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)

# (Task 7a) Button Click
@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower().replace(' ', '-') + '-btn'
    context.driver.find_element_by_id(button_id).click()

# (Task 7b) Text Present
@then('I should see "{text_string}" in the "{element_name}"')
def step_impl(context, text_string, element_name):
    element_id = 'product_' + element_name.lower().replace(' ', '_')
    if element_name == "Product ID":
        element_id = "product_id"
    element = context.driver.find_element_by_id(element_id)
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    assert element.get_attribute('value') == text_string

# (Task 7c) Text NOT Present
@then('I should not see "{text_string}" in the "{element_name}"')
def step_impl(context, text_string, element_name):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    assert element.get_attribute('value') != text_string

# (Task 7d) Message Present
@then('I should see the message "{message}"')
def step_impl(context, message):
    element = context.driver.find_element_by_id('flash_message')
    WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert message in element.text

@then('I should see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element_by_id('search_results')
    assert text in element.text

@then('I should not see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element_by_id('search_results')
    assert text not in element.text

@then('I should see {count} rows in the results')
def step_impl(context, count):
    table = context.driver.find_element_by_id('search_results')
    rows = table.find_elements_by_tag_name('tr')
    assert len(rows) == int(count) + 1 # +1 for header row
