pyghosts
****

In remembrance of "12ghosts" (a handy utility suite of Windows shortcuts - which
I loved), pyghost similarly collects my python shortcuts to common tasks.

pyghosts is both a convenient collection of useful functions which aren't worth
their own repo. pyghosts is a working notebook of python techniques.

There are currently 3 ghosts:

- api_recorder: contains api_recorder, api_remote_controller and api_automock.
- ioioio: contains pinpoint with useful os path tricks.
- stringy: contains btwix to find strings between strings.


Install
=======

Virtual Environment
-------------------

::

  virtualenv --python=python3.5 venv-pyghosts
  source venv-pyghosts/bin/activate

  pip install -r requirements/local.txt


Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  from pyghosts.ghosts.stringy.btwix import btwix

  stwix = stwix('<p>I am btwix. Where are you?</p>', '<p>', '</p>')
  print(stwix)

  >> 'I am btwix. Where are you?'

Release
=======

https://www.kbsoftware.co.uk/docs/


Todo
=======
