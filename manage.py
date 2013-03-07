#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)),'ahgl'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ahgl.settings")

    import ahgl.startup as startup
    startup.run()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
