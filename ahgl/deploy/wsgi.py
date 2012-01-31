import os, sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))

from django.core.handlers.wsgi import WSGIHandler

import pinax.env


# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__, relative_project_path=[os.pardir])

# set application for WSGI processing
application = WSGIHandler()
