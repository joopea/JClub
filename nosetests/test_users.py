import unittest, var, time
from base import BaseTest


class UsersTests(BaseTest):

    # # Login with correct username/password
    # def test_correct_login(self):
    #     self.login(var.u1.username, var.u1.password)

    # # Login with false username/password
    # def test_false_login(self):
    #     self.driver.get(var.home_page)
    #     self.set_text_id('id_user-username', 'Dorien')
    #     self.set_text_id('id_user-password', 'Snuffels')
    #     self.driver.find_element_by_css_selector('input.btn-submit').click()
    #     # Check login was false by looking for error message
    #     self.find_css_element('a.forgot-password-link')

    # def test_empty_login(self):
    #     self.driver.get(var.home_page)
    #     self.driver.find_element_by_css_selector('input.btn-submit').click()
    #     # Check login was empty by looking for error message
    #     self.find_css_element('a.forgot-password-link')

    # def test_create_and_delete_account(self):
    #     # Create account
    #     self.driver.get(var.home_page)
    #     self.driver.find_element_by_css_selector('a.btn.sign-up').click()
    #     self.select_single_item('id_username', '1')
    #     self.set_text_id('id_profile_colour', '#00ffff')
    #     self.select_single_item('id_security_question_1', '1')
    #     self.set_text_id('id_security_answer_1', 'Answer 1')
    #     self.select_single_item('id_security_question_2', '2')
    #     self.set_text_id('id_security_answer_2', 'Answer 2')
    #     self.set_text_id('id_password1', 'asdasd')
    #     self.set_text_id('id_password2', 'asdasd')
    #     self.driver.find_element_by_css_selector('div.form-footer > input.btn-submit').click()
    #     time.sleep(3)

    #     # Delete account
    #     self.driver.find_element_by_css_selector("a.mm-next.mm-fullsubopen").click()
    #     self.driver.find_element_by_link_text('My settings').click()
    #     self.driver.find_element_by_link_text('Delete Profile').click()
    #     self.set_text_id('id_current_password', 'asdasd')
    #     self.driver.find_element_by_css_selector('input.btn-submit').click()

    # def test_follow_unfollow_user(self):
    #     self.login(var.u1.username, var.u1.password)
    #     self.driver.get(var.testing2_user_page)  # Go to u2 profile
    #     self.driver.find_element_by_xpath("//div[@id='post19']/div[3]/div/span[2]/span[2]").click()  # Follow
    #     self.driver.get(var.wall_page)
    #     self.driver.find_element_by_xpath("//div[@id='mm-1']/ul/li[8]/a").click()  # Menu item: people following
    #     self.driver.find_element_by_link_text('testing2').click()  # Check if u2 is there by clicking on u2
    #     self.driver.find_element_by_xpath("//div[@id='post19']/div[3]/div/span[2]/span").click()  # Unfollow
    #     self.driver.find_element_by_css_selector("a.mm-next.mm-fullsubopen").click()
    #     self.driver.find_element_by_link_text("My settings").click()
    #     self.driver.find_element_by_link_text("Following").click()
    #     self.assert_text_with_selector('Users you are following (0)', '#tab3 > h2')  # Check if there are no followed users

    def test_block_unblock_user(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.testing2_user_page)  # Go to u2 profile
        self.driver.find_element_by_xpath("//div[@id='mm-0']/div/div/div[2]/a[2]/span[2]").click()  # Block u2
        self.driver.find_element_by_css_selector("a.mm-next.mm-fullsubopen").click()
        self.driver.find_element_by_link_text("My settings").click()
        self.driver.find_element_by_link_text("Blocked users").click()
        # Check if blocked user == 1 and  if u2 is there
        self.assert_text_with_selector('Blocked users (1)', '#tab4 > h2')
        self.find_text_element('testing2')
        # Logout and login as u2
        self.driver.find_element_by_link_text('Log out of JoopeA').click()
        self.login(var.u2.username, var.u2.password)

        self.driver.get(var.testing1_user_page)
        self.driver.find_element_by_link_text("Comments").click()
        try:
            self.driver.find_element_by_css_selector("input.btn.comment-submit").click()
        except Exception('ElementNotVisibleException'):
            print "Button not found"

        self.driver.find_element_by_css_selector("span.active").click()  # Unblock u2
        self.driver.find_element_by_css_selector("#tab4 > div.form-footer > a.btn.btn-block").click()
        self.driver.find_element_by_link_text("Blocked users").click()
        self.assert_text_with_selector('Blocked users (0)', '#tab4 > h2')  # Check if there are no blocked users

if __name__ == '__main__':
    unittest.main()
