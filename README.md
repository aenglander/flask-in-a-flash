Flask in a Flash
================

This is a example app for Flask utilizing the standard components:

* [Flask](https://flask.palletsprojects.com) for the website
* [Jinja](https://jinja.palletsprojects.com) for templates
* [Click](https://click.palletsprojects.com) for CLI commands

and the optional items:

* [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) for interacting with a database
* [FormEncode](http://www.formencode.org) for form validation

Installation
------------

1. Make sure you have [Pipenv](https://pipenv.kennethreitz.org/en/latest/) setup

2. Run `pipenv install` in the project directory

Running the Site
----------------

Simply run the Flask development server:

Unix Bash (Linux, Mac, etc.):

```
$ export FLASK_APP=todo
$ export FLASK_ENV=development
$ flask run
```

Windows CMD:

```
> set FLASK_APP=todo
> set FLASK_ENV=development
> flask run
```

Windows PowerShell:

```
> $env:FLASK_APP = "todo"
> $env:FLASK_ENV = "development"
> flask run
```

