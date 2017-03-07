#!/usr/bin/env python
import os
import sys

import subprocess

if __name__ == "__main__":

    parent_pid = os.getppid()
    proc = subprocess.Popen('ps aux | grep {parent_pid} | grep python | grep -v grep | wc -l'.format(parent_pid=parent_pid), shell=True, stdout=subprocess.PIPE)
    output = proc.stdout.read()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.locals')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
