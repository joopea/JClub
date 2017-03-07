import cProfile

class ProfileMiddleware(object):
    """
    """
    def process_request(self, request):
        self.prof = cProfile.Profile()
        self.prof.enable()

    def process_response(self, request, response):
        self.prof.disable()
        self.prof.create_stats()
        self.prof.print_stats(sort='tottime')
        return response
