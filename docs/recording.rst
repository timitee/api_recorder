=============
Usage
=============

**Recordings working in isolation**

Like Tests, the goal of Recordings is to make them self-contained units.
Especially if you are recording transactions with a live api (not recommended
unless readonly). That means cleaning up the recording, if possible. It won't
always be possible - but in 99 percent of those occasions it won't matter.

During development you'll be calling those transacations anyway (although you
could you use the recording in a view :-)  Trashing the database with junk test
data is precisely the point of a test api.

So it wouldn't matter if you needed to record the scenario again after
developing the method it tests. Even if the state of the database has changed
since the earlier recording, the new one should provide a single unit of data
to pass the test, and protect it from future errors.

It shouldn't even matter if your recording contains data which has since been
deleted from the api.

Your Recording is custom built for your Test - and while any methods are
decorated @api_recorder, your Test has no other route to the data they posses -
until the method is released from playback.


**Skeleton of a Recording.**

::

  from ghosts.decorators.tests.recording_management import (
      start_recording_scenario,
      end_recording_scenario,
      scenario_exists,
      start_healing_scenario,
      restart_recording_scenario,
  )

  def record_marshall_register_users(can_overwrite):

    if not can_overwrite:
        if scenario_exists(scenario_name):
            return

    start_recording_scenario(scenario_name)
    """The data of methods decorated by the @api_recorder will be recorded."""

    # Call any of the methods decorated by the @api_recorder here


    # Finish recording data for your tests, then ...

    end_recording_scenario(scenario_name)
    """
    All the recordings will be packaged and saved into:

    proj/automocks/
                  mock_<scenario_name>.py
                  redis_<scenario_name>.py
    """


**Example of Recording.**

::

  from ghosts.decorators.tests.recording_management import (
      start_recording_scenario,
      end_recording_scenario,
      scenario_exists,
      start_healing_scenario,
      restart_recording_scenario,
  )

  def record_marshall_register_users(can_overwrite):

    if not can_overwrite:
        """Check if there is a saved recording."""
        if scenario_exists(scenario_name):
            """There is! Ooppps... back up slowly.... """
            return

    start_recording_scenario(scenario_name)

    """Now we start recording some data."""
    for regee in list_of_fake_db_registrees():

        marshall = StockwareCustomerMarshall(0, 0)
        """Recording: .__init__(0, 0)."""

        new_customer_id = marshall.create(
                                regee['name'], regee['address'],
                                regee['postCode'], regee['countryCode']
                                regee['password_1st'])
        """Recording: .create()."""

        marshall.check_password(regee['email'], regee['password_1st'])
        """Recording: .check_password()."""

        customer_dict = {}
        customer_dict['id'] = new_customer_id
        customer_dict['webAccess'] = 'Y'

        marshall.save_all(customer_dict)
        """Recording: .save()."""

        start_healing_scenario(scenario_name)
        """Any methods decorated by the @api_recorder will now act normally, but
        the recorder will pause. We don't want this included in the recording.
        """
        marshall.delete(new_customer_id)
        """Clean up. This may not always be a good idea. Especially if you
        intend to record more against this customer."""

        restart_recording_scenario(scenario_name)
        """Recording will resume. We are in a loop remember :)"""



    end_recording_scenario(scenario_name)


***Use a Recording as the template for a Test.***

First copy and paste your recording into a test_it.py file. Then change:

::

  def record_marshall_register_users(can_overwrite):

To:

::

  def test_marshall_register_users():

... removing the "can_overwrite" parameter.

Don't change!

::

  scenario_name = 'record_marshall_change_passwords'
  """The name recorded must match the test."""

Remove:

::

  if not can_overwrite:
      if scenario_exists(scenario_name):
          return

Change:

::

  start_recording_scenario(scenario_name)

To:

::

  load_scenario(scenario_name)

Ignore the rest for now. At the bottom of the method change:

::

    end_recording_scenario(scenario_name)

To

::

    unload_scenario(scenario_name)
    """Effectively: eject the cassette.

Checklist:

  1) Change "recording_" in method name to "test_"
  2) Leave the scenario_name.
  3) Remove "overwrite" protection.
  4) Change "start_recording_scenario" to "load_scenario".
  5) Leave the rest for now as resources for a test.
  6) Change "end_recording_scenario" to "unload_scenario" as the last.



**Skeleton of a Test.**

::

  from ghosts.decorators.tests.recording_management import (
      load_scenario,
      unload_scenario,
  )

  def test_marshall_register_users(can_overwrite):

    scenario_name = 'record_marshall_change_passwords'
    load_scenario(scenario_name)

    # Start writing your tests here against the recorded data.

    unload_scenario(scenario_name)


**Example of Test.**

For a start, Anywhere it says "Recording:" in the recording method above is
likely to be something whose return value you will want to test stays the same
while you are developing.

So just change "Recording:" to "Testing", run the same command, then test it.

::

  import pytest #etc
  from ghosts.decorators.tests.recording_management import (
      load_scenario,
      unload_scenario,
  )

  def test_marshall_register_users(can_overwrite):

    scenario_name = 'record_marshall_change_passwords'
    load_scenario(scenario_name)

    regee = list_of_fake_db_registrees()[0]
    """Just test one customer."""

    marshall = StockwareCustomerMarshall(0, 0)

    new_customer_id = marshall.create(
                            regee['name'], regee['address'],
                            regee['postCode'], regee['countryCode']
                            regee['password_1st'])
    """Testing: .create()."""

    assert new_customer_id == regee['id']
    """Does the id returned by the method, match the id known."""

    marshall.check_password(regee['email'], regee['password_1st'])
    """Testing: .check_password()."""

    assert marshall.customer_id == regee['id']
    """The customer can log in."""

    unload_scenario(scenario_name)
