============
apirecorder
============

api_recorder is an ambitious attempt to create a method @decorator which can
record, into a database, the return value(s) keyed against the method's identity
and the parameters. You know, like a VCR for python functions, except no one
knows what a VCR is. In this way you could write light api wrappers to consume a
live api and record the returning json responses. These stored responses can
then be played back in tests or when you don't have access to the api.

- Decorate your api wrappers.

- Write and run your Recordings; making all the calls you want to Test at least
  once. Keep them and the recording (in the automocks folder) safe.

- Run your tests with "PlayBack" mode on. The recording gets loaded and played
  back during the test.

**Abstract**

After calling  `start_playingback` the @api_recorder decorator simply maps the
same variables + the signature of the method to retrieve (remember, if you like)
the last lot of data the method returned. Keyed against an api method this would
let you run tests against a set of known responses.

Technically it could be made to handle any serialable method return, but what
would be the point of recording a local method - except to see whether it
changes? I'm using it for an xml-rpc driven api and Flickr's json engine which I
working against for a client and personal project respectively.

I already have all the python low level nodes or plugs into the various api
methods - effectively a thin layer over 3rd party xml-rpc clients and flickrapi.
These sit between my application and the 3rd party. Their data can be considered
"as if from" a direct api call. All these wrappers return pure json; which makes
them ideal for this project.
