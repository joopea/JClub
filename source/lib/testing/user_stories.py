import re

USER_STORIES = {
    01: 'This is the user story with ID 1',
    02: 'This is the user story with ID 2',
    07: 'This is the user story with ID 3',
    04: 'This is the user story with ID 4',
    05: 'This is the user story with ID 5',
    06: 'This is the user story with ID 6',
    03: 'This is the user story with ID 7',
    }


class UserStoriesDocstringParser(object):
    """
    Mixin for parsing docstrings in default Python unittest tests (and everything that extends from it
    """

    @staticmethod
    def get_user_story(user_story_id=None):
        """
        Returns an user story string for the specified user story id
        """

        try:
            user_story = USER_STORIES[user_story_id]
        except KeyError:
            user_story = "ERROR - Could not find a user story with id: {user_story_id}".format(user_story_id=user_story_id)

        return user_story

    def shortDescription(self):
        try:
            user_story_id = int(re.match('@USERSTORY:(.+)$', str(self.__doc__).strip()).group(1))
            user_story = self.get_user_story(user_story_id=user_story_id)
        except AttributeError:
            user_story = "ERROR - No user story ID specified"

        return user_story

    def get_user_story_id(self):
        """
        Parses a tests docstring to extract the user story id
        """
        try:
            user_story_id = int(re.match('@US:(\d+)', str(self.__doc__).strip()).group(1))
        except AttributeError:
            user_story_id = None

        return user_story_id