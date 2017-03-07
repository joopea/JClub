import re


"""
http://stackoverflow.com/questions/22565100/regex-for-accepting-only-persian-characters/22565376#22565376

a username contains
    4 numbers
    1...n of [a-z\u0600-\u06FF\uFB8A\u067E\u0686\u06AF]
        a-z is al letters in our alphabet
        \u0600-\u06FF\uFB8A\u067E\u0686\u06AF is all letters in the persian alphabet

a mention starts with an @
and ends with the username
"""
mention_start_token = "@"

username_regex = (
    "["                                         # any character in the following set
        "\S"
    #     "a-z"                                       # all valid english (26-latin) characters
    #     "\u0600-\u06FF\uFB8A\u067E\u0686\u06AF"     # all valid persian characters
    "]"                                         # end character set
    "+"                                         # one or more of that character set

    "-"

    "\d{1,3}"                                     # four digits
)

regex = re.compile((
    "(" +
        mention_start_token +
        username_regex +
    ")"
))


def find_mentions(text):
    mentions = re.findall(regex, unicode(text))
    return mentions
    # return (name for name in re.findall(regex, text))
