After Hours Gaming League Web Site
==================================

[![Imgur](http://i.imgur.com/XRSju5C.png)](http://afterhoursgaming.tv/)

This is the source for <http://afterhoursgaming.tv/>.

*Want to contribute?* Check out [CONTRIBUTING.md](https://github.com/ahgl/ahgl-site/blob/master/CONTRIBUTING.md)!

Prerequisites
-------------

You should be familiar with
[Python 2.7](http://www.python.org/download/releases/2.7/),
[Django 1.4](https://docs.djangoproject.com/en/1.4/),
and [NodeJS 0.10](http://nodejs.org).
This site also makes use of Redis, Celery, South, Pinax, and a few other things.

### 1. Install the Python dependencies

First, fork this repo by clicking the "Fork" button above. Then clone it locally.

Install pip and virtualenv (you might need to run this as root):

    $ easy_install virtualenv
    $ easy_install pip

Create a virtual environment directory somewhere outside of the repo:

    $ virtualenv --distribute ENV

Source that environment (you might want to add this to your `.bashrc`/`.zshrc`):

    $ . ENV/bin/activate

NOTE: As of Oct 1, 2013, Git versions 1.3 and newer break pip, so you need to install the bleeding-edge version of pip. More info [here](http://oliviercortes.com/pip-and-git-on-the-edge.html).

    $ pip install -U -e git+https://github.com/pypa/pip.git@develop#egg=pip-dev

Install all of the required libraries. This takes a while, so go grab some coffee:

    $ pip install -r requirements.txt

#### Windows users

Visit <http://www.lfd.uci.edu/~gohlke/pythonlibs/> to download the
following precompiled packages:

- psycopg2
- lxml 2.3
- PIL
- greenlet
- cython

Remove the line `lxml==2.3` from `ahgl/requirements.txt` before continuing to the next step.

### 2. Create a local settings file

    $ cp ahgl/local_settings.py.dist ahgl/local_settings.py

`local_settings.py` is sourced by `settings.py` and isn't checked in, so put any changes you need for development in there.

### 3. Prepare the database

* **Mac OS X:** Grab [Postgres.app](http://postgresapp.com/) (easiest) or `brew install postgres` (easy)
* **Debian/Ubuntu:** `sudo apt-get install postgresql`
* **Windows:** Go [here](http://www.postgresql.org/download/windows/)

Create the database:

    $ psql -h localhost
    > create database ahgl;
    CREATE DATABASE

Initialize the tables:

    $ ./manage.py syncdb --noinput
    $ ./manage.py migrate

Load some sample data:

    $ ./manage.py loaddata ahgl/fixtures/dev1.json
    $ ./manage.py loaddata ahgl/fixtures/dev2.json

### 4. Run the Django backend

    $ ./manage.py runserver

### 5. Set up and run the frontend

First, install Grunt and Bower:

    $ npm install -g bower grunt-cli

Then install the frontend dependencies:

    $ cd ahgl/static/js/app
    $ npm install
    $ bower install

Run the frontend:

    $ grunt serve

Now visit http://localhost:9000/ and you should see something that looks like AHGL!

### 6. Log into the admin panel

Go to http://localhost:8000/admin and login with `admin` / `admin`.

**The CMS plugin** edits a lot of the static stuff.

**The profiles/ and tournaments/ directories** have most of the important models and views. Lots of views are the newer Django class-based views.

**The admin view** (http://localhost:8000/admin) is worth poking through.

GLHF!
