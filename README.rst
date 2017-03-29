ghosts
****


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

  from ghosts.stringy.btweex import btweex

  stweex = btweex('<p><b>Hello world</b>. I am <b>btweex</b>. Who the hell are you?</p>', '<p>', '</p>')
  print(stweex)
  >> <b>Hello world</b>. I am <b>btweex</b>. Who the hell are you?

## Samples

See the model folder for ready to use column definitions and models which can
also be used as a base to create your own.

Release
=======

https://www.kbsoftware.co.uk/docs/


Todo
=======
