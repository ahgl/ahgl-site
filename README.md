AHGL - After Hours Gaming League
================================

This is the source for <http://afterhoursgaming.tv/>

Platform
--------

This site is built upon the following basic platform:

- python
- django
- postgres - relational database
- redis - for caching
- celery - for task queue
- south - for database migrations

Setup
-----

To setup an environment to test locally, you should first install
[Python (2.7)](http://python.org/),
[pip](http://pypi.python.org/pypi/pip), and
[virtualenv](http://pypi.python.org/pypi/virtualenv) as well as
[PostgreSQL](http://postgresql.com) (although you can use SQLite if
necessary).

Pip is the python package management tool that will allow you to install
all the other python libraries that are used quite easily. Virtualenv
allows you to have segregated python installs that have different
libraries.

Create a virtual env:

    $ virtualenv --distribute ENV

Start that environment:

    $ ENV/Scripts/activate

Windows - execute the windows only setups below

Now install the python libraries using pip:

    $ pip install --requirement=ahgl/requirements/project.txt

You'll want to create a local\_settings.py file to specify your settings
based on your local setup:

    $ cp ahgl/local_settings.py{.dist,}

Then edit it to verify/change any of the options.

If all of that worked, you should be able to initialize the database by
running from the ahgl folder (note: you might need to run syncdb twice):

    $ ./manage.py syncdb
    $ ./manage.py syncdb
    $ ./manage.py migrate

Initialize the database with some sample data:

    $ ./manage.py loaddata fixtures/sample_data.json

Create the default Django Site object:

    $ ./manage.py shell
    >>> from django.contrib.sites.models import Site
    >>> Site.objects.create(name='example.com', domain='example.com')

Now that everything is setup, you can run the local service:

    $ ./manage.py runserver

Now visit localhost:8000/admin and you should see a web page appear!

### Windows only

Install precompiled packages:

Visit <http://www.lfd.uci.edu/~gohlke/pythonlibs/> to download the
following packages

- psycopg2
- lxml 2.3
- PIL
- greenlet
- cython

Also download git at <http://git-scm.com/>

Use easy\_install to install them in the virtual environment:

    $ easy_install "filename.exe"

Remove the line "lxml==2.3" from ahgl/requirements/project.txt before
continuing to the next step
