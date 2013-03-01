#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)),'apps'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ahgl.settings")

    import env
    # setup the environment for Django and Pinax
    env.setup_environ(__file__)

    #import ahgl.startup as startup
    #startup.run()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
