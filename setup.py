"""
This is to define the project so that it's packages can be installed.

https://docs.python.org/3.8/distutils/setupscript.html
"""

from distutils.core import setup

setup(name='todo',
      version='1.0',
      description='Flask in a Flash: To Do List',
      author='Adam Englander',
      author_email='adamenglander@yahoo.com',
      url='https://github.com/aenglander/flask-in-a-flash',
      packages=['todo'],
      )
