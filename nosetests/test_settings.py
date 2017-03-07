import unittest, var
from base import BaseTest


class SettingsTests(BaseTest):
    # Login with correct username/password
    def test_profile_settings(self):
        # Login, go to settings ad change profile colour
        self.login(var.u2.username, var.u2.password)
        self.driver.find_element_by_css_selector('a.mm-next.mm-fullsubopen').click()
        self.driver.find_element_by_link_text('My settings').click()
        self.set_text_id('id_profile_colour', '#ff0000')
        self.driver.find_element_by_css_selector('input.btn-submit').click()

        # Check if change was successful
        try:
            self.assertEqual("#ff0000", self.driver.find_element_by_id("id_profile_colour").get_attribute("value"))
        except AssertionError as e:
            self.verificationErrors.append(str(e))

        # Change back
        self.set_text_id('id_profile_colour', '#000000')
        self.driver.find_element_by_css_selector('input.btn-submit').click()

if __name__ == '__main__':
    unittest.main()
