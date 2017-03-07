import time
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import StaleElementReferenceException
from lib.testing.selenium.mixins import AuthenticatedSeleniumTestCaseMixin
from lib.testing.user_stories import UserStoriesDocstringParser
from lib.testing.helpers import ScenarioTestCaseMixin, HelperTestCaseMixin
from selenium import webdriver


class SeleniumTestRunner(StaticLiveServerTestCase):
    """
    Base Selenium Test Runner class, responsible for the core (not Django specific) Selenium functionality
    """
    helpers = []
    helper = None
    scenario = None
    selenium = None
    webdriver = settings.TEST_SELENIUM_DRIVER

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Firefox() #Chrome(executable_path=cls.webdriver)
        #cls.selenium = webdriver.Chrome(executable_path=cls.webdriver)
        super(SeleniumTestRunner, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestRunner, cls).tearDownClass()

    def open(self, url=None, view=None, **kwargs):
        """
        Open a page with the self.selenium instance
        :param page: Page name as specified in urls.py
        :param kwargs: arguments required to resolve the url
        """
        if url is None:
            url = str(reverse(view, kwargs=kwargs))

        self.selenium.get(str(self.live_server_url) + url)

    def click_through_to_new_page(self, css_selector):
        """
        Click on an element and wait until until the page is loaded.

        By default Selenium sessions are destroyed after Selenium sends the last command (e.g click on link)
        without waiting for an response.
        Because the tests are run threaded this raises some exceptions on the server level, this function forces Selenium
        to wait until the page is loaded.
        """
        link = self.selenium.find_element_by_css_selector(css_selector)
        link.click()

        def link_has_gone_stale():
            try:
                # poll the link with an arbitrary call
                link.find_elements_by_id('doesnt-matter')
                return False
            except StaleElementReferenceException:
                return True

        self.wait_for(link_has_gone_stale)

    def wait_for(self, condition_function, max_seconds=3):
        end_time = time.time() + max_seconds

        while True:
            if condition_function():
                break
            if time.time() >= end_time:
                raise Exception('Timeout waiting for {}'.format(condition_function.__name__))
            time.sleep(0.1)

        return True


class ConcreteSeleniumTestRunner(UserStoriesDocstringParser,
                                 HelperTestCaseMixin,
                                 ScenarioTestCaseMixin,
                                 AuthenticatedSeleniumTestCaseMixin,
                                 SeleniumTestRunner):
    pass
