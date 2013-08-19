After Hours Gaming League Web Site
==================================

This is the source for <http://afterhoursgaming.tv/>

Getting Started
---------------

You should be familiar with [Python 2.7](http://www.python.org/download/releases/2.7/)
and [Django 1.4](https://docs.djangoproject.com/en/1.4/). This site also makes use of Redis, Celery, South, Pinax, and a few other things.

### 1. Install the Python dependencies

First install pip and virtualenv (you might need to run this as root):

    $ easy_install virtualenv
    $ easy_install pip

Create a virtual env in an arbitrary directory, `ENV`:

    $ virtualenv --distribute ENV

Source that environment (you might want to add this to your `.bashrc`/`.zshrc`):

    $ . ENV/bin/activate

Install all of the required libraries, which takes a while:

    $ pip install --requirement=ahgl/requirements/project.txt

#### Windows users

Visit <http://www.lfd.uci.edu/~gohlke/pythonlibs/> to download the
following precompiled packages:

- psycopg2
- lxml 2.3
- PIL
- greenlet
- cython

Use easy\_install to install them in the virtual environment:

    $ easy_install "filename.exe"

Remove the line "lxml==2.3" from ahgl/requirements/project.txt before
continuing to the next step

### 2. Create a local settings file

    $ cp ahgl/local_settings.py.dist ahgl/local_settings.py

`local_settings.py` is sourced by `settings.py` and isn't checked in, so put any changes you need for development in there.

### 3. Prepare the database

* **Mac OS X:** Grab [Postgres.app](http://postgresapp.com/) (easiest) or `brew install postgres` (easy)
* **Debian/Ubuntu:** `sudo apt-get install postgresql`
* **Windows:** Go [here](http://www.postgresql.org/download/windows/)

Then (yes, you might need to run `syncdb` twice):

    $ ./manage.py syncdb
    $ ./manage.py syncdb
    $ ./manage.py migrate

Load some sample data:

    $ ./manage.py loaddata fixtures/dev.json

### 4. Run the server

    $ ./manage.py runserver

Now visit http://localhost:8000/ and you should see something that looks like AHGL!

### 5. Log into the admin panel

Go to http://localhost:8000/admin and login with the username and password `admin`. 

Where Do I Start?
-----------------

**The CMS plugin** edits a lot of the static stuff.


