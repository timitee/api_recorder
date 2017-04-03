# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.ioioio.pinpoint import project_path
from ghosts.api_recorder.tests.recording_management import TheMC
from ghosts.api_recorder.api_recorder import api_recorder
from ghosts.api_recorder.api_controller import ApiRecorderController

@api_recorder
def addit(x, y):
    return x + y


mc = TheMC()
arc = ApiRecorderController('', '')
mc = TheMC()
mc.off()
mc.mock()
mc.rec()
mc.mock()


def test_the_mc():

    mc = TheMC()
    arc = ApiRecorderController('', '')

    mc.off()
    assert arc.power == ApiRecorderController.POWER_OFF

    mc.rec()
    assert arc.run_mode == ApiRecorderController.RECORDING

    mc.mock()
    assert arc.mocks == ApiRecorderController.MOCKING_ON

    mc.kind()
    assert arc.mocks == ApiRecorderController.MOCKING_OFF

    mc.shutdown()



def test_the_mc_sample():

    mc = TheMC()
    arc = ApiRecorderController('', '')

    mc.kind()

    addit(3, 4)

    mocks_path = os.path.join(project_path(), 'automocks')
    module_name = 'mock_{}__{}.py'.format(mc.master_name, mc.master_name)
    mock_file = os.path.join(mocks_path, module_name)

    assert not os.path.exists(mock_file)
    """Has our mock file been created?"""

    mc.shutdown()
