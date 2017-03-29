# -*- encoding: utf-8 -*-
import os
import pytest
from ghosts.ioioio.pinpoint import *

path_being_mapped = ['pyghosts', 'ghosts', 'ioioio', 'tests', 'test_pinpoint.py']



def test_pinpoint_projectfile_fullpath():

    testing_path = projectfile_fullpath(__file__)

    assert testing_path.split(os.sep)[-5:] == path_being_mapped


def test_pinpoint_projectfile_path():

    testing_path = projectfile_path(__file__)

    assert testing_path.split(os.sep)[-4:] == path_being_mapped[:-1]


def test_pinpoint_projectfile_filename_ext():

    testing_path = projectfile_filename_ext(__file__)

    assert testing_path == 'test_pinpoint.py'


def test_pinpoint_projectfile_filename():

    testing_path = projectfile_filename(__file__)

    assert testing_path == 'test_pinpoint'


def test_pinpoint_projectfile_ext():

    testing_path = projectfile_ext(__file__)

    assert testing_path == '.py'


def test_pinpoint_projectfile_folder():

    testing_path = projectfile_folder(__file__)

    assert testing_path.split(os.sep)[-4:] == path_being_mapped[:-1]


def test_pinpoint_projectfile_apppath():

    testing_path = projectfile_apppath(__file__)

    assert testing_path.split(os.sep)[-2:] == path_being_mapped[:-3]


def test_pinpoint_projectfile_projectpath():

    testing_path = projectfile_projectpath(__file__)

    assert testing_path.split(os.sep)[-1] == 'pyghosts'
