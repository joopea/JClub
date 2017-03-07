"""

"""
import os

from fabric.api import env
from jinja2 import Environment, ChoiceLoader, PackageLoader, FileSystemLoader

from deployscript.commands import *

import project


env.fab_path = lambda base: os.path.abspath(os.path.join(os.path.dirname(__file__), str(base)).replace('\\','/'))

env.jinja = Environment(loader=ChoiceLoader([
        FileSystemLoader(env.fab_path('templates')),
        PackageLoader('deployscript', 'templates'),
    ]))
