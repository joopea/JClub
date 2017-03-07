#reference views
#vermeld even welke je wel/niet support zodat als je ze mist ze gemakkelijk toe te voegen zijn later

# from django.views.generic.base import View, TemplateView, RedirectView
# from django.views.generic.dates import (ArchiveIndexView, YearArchiveView, MonthArchiveView,
#                                         WeekArchiveView, DayArchiveView, TodayArchiveView,
#                                         DateDetailView)
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
# from django.views.generic.list import ListView

from django import test
from django.test import Client
from lib.testing.user_stories import UserStoriesDocstringParser


class DjangoTestRunner(UserStoriesDocstringParser, test.TestCase):
    """
    Concrete Django Test Runner implementation, provides core functionality required for tests
    """

    client = Client()

    def assert_page_status_code(self, url=None, status_code=200):
        self.assertEqual(self.client.get(url).status_code, status_code)

    def assert_form_submit_status_code(self, url=None, form_data=None, status_code=200):
        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, status_code)


class GenericViewsTestRunner(DjangoTestRunner):

    url = None
    url_arguments = {}
    form_data = None
    scenarios = []

    def handle_scenarios(self):
        for scenario in self.scenarios:
            scenario().create(test_scenario=scenario.default)

    def setUp(self, *args, **kwargs):
        super(GenericViewsTestRunner, self).setUp()

        self.handle_scenarios()
