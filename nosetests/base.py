from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
import unittest
import var  # var contains the variables


class AsUser1(object):
    def setUp(self, *args, **kwargs):
        super(AsUser1, self).setUp(*args, **kwargs)
        self.login(var.u1)


class AsUser2(object):
    def setUp(self, *args, **kwargs):
        super(AsUser2, self).setUp(*args, **kwargs)
        self.login(var.u2)


class BaseTest(unittest.TestCase):

    # Setup
    def setUp(self, *args, **kwargs):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        self.verificationErrors = []
        self.accept_next_alert = True

    def _create_user(self, user, user_data):
        self.driver.get(var.home_page)
        self.driver.find_element_by_css_selector('a.btn.sign-up').click()
        self.select_single_item('id_username', user_data['id_username'])
        self.set_text_id('id_profile_colour', user_data['id_profile_colour'])
        self.select_single_item('id_security_question_1', user_data['id_security_question_1'])
        self.set_text_id('id_security_answer_1', user_data['id_security_answer_1'])
        self.select_single_item('id_security_question_2', user_data['id_security_question_2'])
        self.set_text_id('id_security_answer_2', user_data['id_security_answer_2'])
        self.set_text_id('id_password1', user_data['id_password1'])
        self.set_text_id('id_password2', user_data['id_password2'])
        self.driver.find_element_by_css_selector('div.form-footer > input.btn-submit').click()

    # Login with correct data
    def login(self, user):
        self.driver.get(var.home_page)
        self.set_text_id('id_user-username', user.username)
        self.set_text_id('id_user-password', user.password)
        self.driver.find_element_by_css_selector('input.btn-submit').click()
        # Check if login was succesful by getting username
        self.find_text_element('Log out of JoopeA')

    def admin_login(self, username, password):
        self.driver.get(var.admin_page)
        self.set_text('id_username', username)
        self.set_text('id_password', password)
        self.driver.find_element_by_css_selector('input.grp-button.grp-default').click()

    def set_text_id(self, field_id, text):
        self.driver.find_element_by_id(field_id).clear()
        self.driver.find_element_by_id(field_id).send_keys(text)

    def set_text_name(self, field_name, text):
        self.driver.find_element_by_name(field_name).clear()
        self.driver.find_element_by_name(field_name).send_keys(text)

    def set_text_selector(self, selector, text):
        self.driver.find_element_by_css_selector(selector).clear()
        self.driver.find_element_by_css_selector(selector).send_keys(text)

    def find_css_element(self, selector_id):
        try:
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR, selector_id))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def find_text_element(self, text):
        try:
            self.assertTrue(self.is_element_present(By.LINK_TEXT, text))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def assert_text_with_xpath(self, value, find_xpath):
        try:
            self.assertEqual(value, self.driver.find_element_by_xpath(find_xpath).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def assert_text_with_selector(self, text, selector_id):
        try:
            self.assertEqual(text, self.driver.find_element_by_css_selector(selector_id).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def select_single_item(self, field_id, value):
        Select(self.driver.find_element_by_id(field_id)).select_by_value(value)

    def select_multi_items(self, field_id, *values):
        options = Select(self.driver.find_element_by_id(field_id))
        for value in values:
            options.select_by_value(value)

    def select_all_items(self, field_id):
        options = Select(self.driver.find_element_by_id(field_id)).options
        for option in options:
            if not option.is_selected():
                option.click()

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    # Close browser
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
