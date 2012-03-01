This site is built upon the following basic platform:
	-python
	-django
	-postgres - relational database
	-redis - for caching
	-celery - for task queue
	-south - for database migrations

To setup an environment to test locally, you should first install python (2.7) http://python.org/, pip http://pypi.python.org/pypi/pip and virtualenv http://pypi.python.org/pypi/virtualenv as well as postgres (although you can use sqlite if necessary).

Pip is the python package management tool that will allow you to install all the other python libraries that are used quite easily. Virtualenv allows you to have segregated python installs that have different libraries. Once you have these installed,
	Create a virtual env:
	virtualenv --distribute ENV
	Start that environment:
	ENV/Scripts/activate
	
	Now install the python libraries using pip:
	pip install --requirement=ahgl/requirements/project.txt
	
	You'll want to create a local_settings.py file to specify your settings based on your local setup. This will likely need these sections:
# You'll need this section to specify your caching - if you don't want to setup redis, this is a lazy way that just uses in-place memoroy. You will still have to specify the redis server here if you do it.	
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ahgl'
    }
}

# point to your databse. If you use sqlite keep in mind that many database things might not work in production.
DATABASES = {
    "default": {
        "ENGINE": "postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "ahgl",                       # Or path to database file if using sqlite3.
        "USER": "username",                             # Not used with sqlite3.
        "PASSWORD": "password",                         # Not used with sqlite3.
        "HOST": "localhost",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

COMPRESS = False

# This is the default celery setup, if you installed redis it is recommended to use it as the backend instead of the database.
CELERY_RESULT_BACKEND = "database"
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

	If all of that worked, you should be able to initialize the database by running from the ahgl folder:
	python manage.py syncdb
	python manage.py migrate
	
	Now that everything is setup, you can run the local service:
	python manage.py runserver
	
	Now visit localhost and you should see a web page appear!