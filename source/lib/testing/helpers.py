class ScenarioRunnerHelper(object):
    pass


class TestRunnerHelper(object):
    pass


class ScenarioTestCaseMixin(object):
    """
    This mixin creates scenarios for every scenario listed
    on the class with a with_<scenario_name> using the cls.scenarios class
    and adds the helper functions to cls.scenario
    """
    scenarios = []
    scenario = None

    @classmethod
    def setUpClass(cls):
        super(ScenarioTestCaseMixin, cls).setUpClass()
        cls.setupScenarios()

    @classmethod
    def setupScenarios(cls):
        cls.scenario = ScenarioRunnerHelper()
        for scenario in cls.scenarios:
            inst = scenario()
            setattr(cls.scenario, inst.name, inst)

            items_to_create = getattr(cls, 'with_' + inst.name)
            for item in items_to_create:
                inst.create(item)


class HelperTestCaseMixin(object):
    """
    This mixin initialize all the test helpers listed in cls.helpers to the cls.helper function.
    """

    helpers = []
    helper = None

    @classmethod
    def setUpClass(cls):
        super(HelperTestCaseMixin, cls).setUpClass()
        cls.setupHelpers()

    @classmethod
    def setupHelpers(cls):
        cls.helper = TestRunnerHelper()
        for helper in cls.helpers:
            inst = helper(selenium=cls.selenium)
            setattr(cls.helper, inst.name, inst)


class ScenarioHelperBase(object):
    """
    BaseClass for scenario helpers
    """
    form = None
    data = {}
    test_data = {}

    def __getitem__(self, item):
        return self.data[item]

    @staticmethod
    def prepare_form_data(test_data):
        """
        Split test_data in a data_dict and a file_dict

        To upload an file using an Django form we have to use a multipart dict,
        in order to do it in code we have to split the data in two different dicts,
        one with the data, one with the files.
        """
        data = {
            'form': {},
            'file': {},
        }

        for key, value in test_data.iteritems():
            item = value
            data_type = 'form'
            if value.__class__.__name__ == 'TestFile':
                data_type = 'file'
                item = value.file

            data[data_type] = item

        return data

    def create(self, test_scenario):
        data = self.prepare_form_data(test_data=self.test_data[test_scenario])
        form = self.form(data['form'], data['file'])
        self.data[test_scenario] = form.save()
