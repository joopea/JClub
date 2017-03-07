import unittest, var
from base import BaseTest


class PostTests(BaseTest):
    def test_1_create_post_on_own_wall(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.find_element_by_link_text('New Post').click()
        self.set_text_id('id_title', 'Test')
        self.driver.execute_script("CKEDITOR.instances['id_message'].setData('Dit is een testbericht. Ok doei.')")
        self.driver.find_element_by_css_selector('input.btn.comment-submit').click()

        # Go to wall to see if post was succes
        self.driver.get(var.wall_page)
        self.assert_text_with_selector('Test', 'h2.post-title')

    def test_2_delete_post_on_own_wall(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.wall_page)
        self.driver.find_element_by_css_selector('a.remove-post-button.post-button').click()
        self.driver.find_element_by_name('yes_no').click()

    def test_3_create_comment_on_post(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.post_page)
        self.set_text_name('message', 'Test comment')
        self.driver.find_element_by_css_selector('input.btn.comment-submit').click()
        self.assert_text_with_selector('Test comment', 'div.comment-content > p')

    def test_4_delete_comment_on_post(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.post_page)
        self.driver.find_element_by_css_selector('span.delete-button.fright').click()
        self.driver.find_element_by_name('yes_no').click()

    def test_5_like_unlike_post(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.post_page)
        self.assert_text_with_xpath("Like", "//div[@id='post19']/div[3]/div/a/span[2]")
        self.driver.find_element_by_xpath("//div[@id='post19']/div[3]/div/a/span[2]").click()
        self.assert_text_with_xpath("Unlike", "//div[@id='post19']/div[3]/div/a/span")
        self.driver.find_element_by_xpath("//div[@id='post19']/div[3]/div/a/span").click()
        
    # Not ready
    # def test_6_share_post(self):
    #     self.login(var.u1.username, var.u1.password)
    #     self.driver.get(var.post_page)

    def test_7_save_unsave_post(self):
        self.login(var.u1.username, var.u1.password)
        self.driver.get(var.post_page)
        self.driver.find_element_by_xpath("//div[@id='post19']/div/a/span[2]/span/i[2]").click()
        self.driver.find_element_by_link_text('Saved Posts').click()
        self.assert_text_with_selector('Test', 'h2.post-title')
        self.driver.find_element_by_xpath("//div[@id='post19']/div/a/span/span/i[2]").click()
        # TODO: verify if post is no longer saved

    # Not ready
    # def test_8_report_post(self):
    #     self.login(var.u1.username, var.u1.password)
    #     self.driver.get(var.post_page)

if __name__ == '__main__':
    unittest.main()
