class FormException(Exception):
    pass


class FormUnknownFieldException(FormException):
    pass


class FormValidationException(FormException):
    pass


class FormInputException(FormException):
    pass