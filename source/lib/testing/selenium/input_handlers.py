from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select


class InputHandler(object):
    error_class = ".errorlist"

    def __init__(self, selector='', selenium=None):
        self.selector = selector
        self.selenium = selenium

    def fill(self, value=None):
        raise NotImplementedError

    def clear(self):
        self.selenium.find_element_by_id(self.selector).clear()

    def get_value(self):
        return self.selenium.find_element_by_id(self.selector).get_attribute('value')

    def get_error(self):
        try:
            error = self.selenium.find_element_by_css_selector(
                "#{selector} + {error_class} ".format(**{
                    'selector': self.selector,
                    'error_class': self.error_class,
                })
            ).text
        except NoSuchElementException:
            error = False

        return error


class SeleniumTextInputHandler(InputHandler):
    def fill(self, value=None):
        self.selenium.find_element_by_id(self.selector).send_keys(value)


class SeleniumFileInputHandler(InputHandler):

    def fill(self, value=None):
        self.selenium.find_element_by_id(self.selector).send_keys(value.location)


class SeleniumSelectInputHandler(InputHandler):

    def fill(self, value=None):
        Select(self.selenium.find_element_by_id(self.selector)).select_by_visible_text(value)

    def clear(self):
        Select(self.selenium.find_element_by_id(self.selector)).deselect_all()

    def get_value(self):
        Select(self.selenium.find_element_by_id(self.selector)).all_selected_options()


class SeleniumInputHandlerFactory():
    """
    Factory to handle Django form widgets, returns an Selenium Input Handler
    """
    input_handler_mapping = {
        'TextInput': SeleniumTextInputHandler,
        'EmailInput': SeleniumTextInputHandler,
        'URLInput': SeleniumTextInputHandler,
        'NumberInput': SeleniumTextInputHandler,
        'PasswordInput': SeleniumTextInputHandler,
        'Textarea': SeleniumTextInputHandler,

        'ClearableFileInput': SeleniumFileInputHandler,

        'Select': SeleniumSelectInputHandler
    }

    @classmethod
    def get_input_handler(cls, widget_type=None, selector='', selenium=None):
        return cls.input_handler_mapping[widget_type](selector=selector, selenium=selenium)
