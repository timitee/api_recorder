api_recorder
****

Function decorator to record and playback json/other api calls. Useful for
preparing mocks from live data for testing, or for monitoring the activity
of a 3rd party api during developing.

- api_recorder: contains api_recorder, api_remote_controller and api_automock.


Install
=======

Virtual Environment
-------------------

::

  virtualenv --python=python3.5 venv-api_recorder
  source venv-api_recorder/bin/activate

  pip install -r requirements/local.txt


Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

See docs


Release
=======

https://www.kbsoftware.co.uk/docs/


Todo
=======
