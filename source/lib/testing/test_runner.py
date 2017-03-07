import json
from unittest import TextTestResult, TextTestRunner
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.test.runner import DiscoverRunner
from lib.testing.user_stories import USER_STORIES
from unittest.case import TestCase


class NotATestException(Exception):
    pass


class StoreTestResults(TextTestResult):
    """
    Custom TextTestResult class that stores the results
    """

    results = {'success': [],
               'error': [],
               'failure': [],
               'skip': [],
               'expected_failure': [],
               'unexpected_success': []
    }

    def store_results(self, test, status):

        self.results[status].append({
            'class': test.__class__.__name__,
            'test_name': test._testMethodName,
            'user_story_id': getattr(test, 'get_user_story_id', None),
            'user_story': test.shortDescription(),
        })

    def addSuccess(self, test):
        super(TextTestResult, self).addSuccess(test)
        self.store_results(test=test, status='success')

    def addError(self, test, err):
        super(TextTestResult, self).addError(test, err)
        self.store_results(test=test, status='error')

    def addFailure(self, test, err):
        super(TextTestResult, self).addFailure(test, err)
        self.store_results(test=test, status='failure')

    def addSkip(self, test, reason):
        super(TextTestResult, self).addSkip(test, reason)
        self.store_results(test=test, status='skip')

    def addExpectedFailure(self, test, err):
        super(TextTestResult, self).addExpectedFailure(test, err)
        self.store_results(test=test, status='expected_failure')

    def addUnexpectedSuccess(self, test):
        super(TextTestResult, self).addUnexpectedSuccess(test)
        self.store_results(test=test, status='unexpected_success')


class StoreResultsTestRunner(TextTestRunner):
    """
    Custom test runner that stores the results
    """
    resultclass = StoreTestResults


class ConcreteDiscoverRunner(DiscoverRunner):
    """
    Django test runner that exports the results to JSON format
    """

    @staticmethod
    def get_results_summary(results):
        """
        This function returns a summary of the results when given test results
        :param results: StoreResultsTestRunner instance
        :return: dic summary of the results
        """

        covered_user_stories = []
        uncovered_user_stories = []

        for user_story_id, user_story in USER_STORIES.iteritems():
            for category in results:
                for result in results[category]:
                    if result['user_story_id'] == user_story_id:
                        covered_user_stories.append(user_story_id)

        for user_story_id, user_story in USER_STORIES.iteritems():
            if user_story_id not in covered_user_stories:
                uncovered_user_stories.append(user_story_id)

        # We use set to create a distinct array from uncovered_user_stories so that the covered percentage
        # works even if you have multiple tests for the same user story
        percentage = float(len(set(uncovered_user_stories)))/float(len(USER_STORIES)) * float(100)

        summary = {
            'percentage_covered': percentage,
            'covered_user_stories': covered_user_stories,
            'uncovered_user_stories': uncovered_user_stories,
        }

        return summary

    def suite_result(self, suite, result, **kwargs):
        """
        Extended from parent with JSON export functionality
        :param suite: default testrunner test suite
        :param result: StoreResultsTestRunner instance
        """
        result.results['results'] = self.get_results_summary(results=result.results)

        with open(settings.PROJECT_DIR('') + '/test_results.json', 'w') as outfile:
            json.dump(result.results, outfile, sort_keys=True, indent=4)

        t = get_template('test/test_results.html')
        c = Context(result.results)

        with open(settings.PROJECT_DIR('') + '/test_results.html', 'w') as outfile:
            outfile.write(t.render(c))

        super(ConcreteDiscoverRunner, self).suite_result(suite, result, **kwargs)

    def run_suite(self, suite, **kwargs):
        """
        Run the unittest2 test suite with a custom test runner (StoreResultsTestRunner) so we can store the results.
        The default testrunner streams the results to the console, we need all the results in order to export them
        :param suite: default testrunner test suite
        :return: returns an StoreTestResults instance
        """
        return StoreResultsTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)
