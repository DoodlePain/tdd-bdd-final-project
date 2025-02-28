# features/steps/web_steps.py

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('the following products')
def step_impl(context):
    """ Load the database with products """
    headers = {"Content-Type": "application/json"}
    context.resp = context.client.delete('/products/reset')
    assert context.resp.status_code == 204
    for row in context.table:
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": float(row['price']),
            "available": row['available'] == "True",
            "category": row['category']
        }
        context.resp = context.client.post('/products', json=payload, headers=headers)
        assert context.resp.status_code == 201

@when('I visit the "{page_name}"')
def step_impl(context, page_name):
    """ Visit a page by name """
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert message in context.driver.title

@then('I should not see "404 Not Found"')
def step_impl(context):
    """ Check that the page does not contain "404 Not Found" """
    assert "404 Not Found" not in context.driver.page_source

@when('I set the "{field_name}" to "{value}"')
def step_impl(context, field_name, value):
    """ Set a field to a value """
    element = context.driver.find_element(By.NAME, field_name)
    element.clear()
    element.send_keys(value)

@when('I select "{value}" in the "{field_name}" dropdown')
def step_impl(context, value, field_name):
    """ Select a value in a dropdown """
    element = Select(context.driver.find_element(By.NAME, field_name))
    element.select_by_visible_text(value)

@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    """ Press a button """
    button = context.driver.find_element(By.XPATH, f"//button[text()='{button_name}']")
    button.click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    """ Check for a message """
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert"))
    )
    assert message in element.text

@when('I copy the "{field_name}" field')
def step_impl(context, field_name):
    """ Copy the value of a field """
    element = context.driver.find_element(By.NAME, field_name)
    context.clipboard = element.get_attribute("value")

@when('I press the "Clear" button')
def step_impl(context):
    """ Press the Clear button """
    button = context.driver.find_element(By.XPATH, "//button[text()='Clear']")
    button.click()

@then('the "{field_name}" field should be empty')
def step_impl(context, field_name):
    """ Check that a field is empty """
    element = context.driver.find_element(By.NAME, field_name)
    assert element.get_attribute("value") == ""

@when('I paste the "{field_name}" field')
def step_impl(context, field_name):
    """ Paste the value into a field """
    element = context.driver.find_element(By.NAME, field_name)
    element.clear()
    element.send_keys(context.clipboard)

@then('I should see "{value}" in the "{field_name}" field')
def step_impl(context, value, field_name):
    """ Check the value of a field """
    element = context.driver.find_element(By.NAME, field_name)
    assert element.get_attribute("value") == value

@then('I should see "{value}" in the "{field_name}" dropdown')
def step_impl(context, value, field_name):
    """ Check the value of a dropdown """
    element = Select(context.driver.find_element(By.NAME, field_name))
    selected_option = element.first_selected_option
    assert selected_option.text == value
