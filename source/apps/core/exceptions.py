
class JsonResponseException(Exception):
    status_code = 500

    def __init__(self, message=None):
        Exception.__init__(self, message or '')


class Json404(JsonResponseException):
    status_code = 404

    def __init__(self, message=None):
        Exception.__init__(self, message or 'Not found')


class JsonNotFound(Json404):
    def __init__(self, message=None):
        Exception.__init__(self, message or 'Record not found')


class Json405(JsonResponseException):
    status_code = 405

    def __init__(self, message=None):
        Exception.__init__(self, message or 'Not found')
