AHGL - After Hours Gaming League
================================

This is the source for http://afterhoursgaming.tv/

Platform
--------
This site is built upon the following basic platform:

* python
* django
* postgres - relational database
* redis - for caching
* celery - for task queue
* south - for database migrations

Setup
-----
To setup an environment to test locally, you should first install `Python (2.7)
<http://python.org/>`_, `pip <http://pypi.python.org/pypi/pip>`_, and
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ as well as `PostgreSQL
<http://postgresql.com>`_ (although you can use SQLite if necessary).

Pip is the python package management tool that will allow you to install all the
other python libraries that are used quite easily. Virtualenv allows you to have
segregated python installs that have different libraries.

Create a virtual env::

    $ virtualenv --distribute ENV

Start that environment::

    $ ENV/Scripts/activate
    
Windows - execute the windows only setups below
    	
Now install the python libraries using pip::

    $ pip install --requirement=ahgl/requirements/project.txt
	
You'll want to create a local_settings.py file to specify your settings based on
your local setup::

    $ cp ahgl/local_settings.py{.dist,}

Then edit it to verify/change any of the options.

If all of that worked, you should be able to initialize the database by running
from the ahgl folder::

    $ ./manage.py syncdb
    $ ./manage.py migrate

Initialize the database with some sample data::

    $ ./manage.py loaddata fixtures/initial_data.json
	
Now that everything is setup, you can run the local service::

    $ ./manage.py runserver
	
Now visit localhost:8000/admin and you should see a web page appear!

Windows only
````````````
Install precompiled packages::

Visit http://www.lfd.uci.edu/~gohlke/pythonlibs/ to download the following packages

* psycopg2
* lxml 2.3
* PIL
* greenlet
* cython

Also download git at http://git-scm.com/

Use easy_install to install them in the virtual environment::

    $ easy_install "filename.exe"
    
Remove the line "lxml==2.3" from ahgl/requirements/project.txt before continuing to the next step
