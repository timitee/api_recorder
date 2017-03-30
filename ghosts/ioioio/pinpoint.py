# -*- encoding: utf-8 -*-
"""Pinpoints a file path given the __name__ of the calling module.


**Usage**

Example coded on home/repo/drawing_app/draw/smart_draw.py:

::

    from pyghosts.ioioio.pinpoint import projectfile_fullpath


    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

    print(projectfile_fullpath(__file__))
    >> home/repo/drawing_app/draw

"""

import os


def _is_yaml_folder(known_path):
    """Utility: Reports whether the known_path has a setup.yaml file."""

    return os.path.exists(os.path.join(known_path, 'setup.yaml'))


def projectfile_fullpath(project_file):
    """A "projectfile" is the starting point. Expects the calling __file__.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/draw/smart_draw.py
    """

    return os.path.realpath(project_file)


def projectfile_filename_ext(project_file):
    """The filename and file extension.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> smart_draw.py
    """

    _known_path = projectfile_fullpath(project_file)

    return os.path.split(_known_path)[1]


def projectfile_filename(project_file):
    """The name of the file without extension.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> smart_draw
    """

    _filename_ext = projectfile_filename_ext(project_file)

    return os.path.splitext(_filename_ext)[0]


def projectfile_ext(project_file):
    """The file extension.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> .py
    """

    _filename_ext = projectfile_filename_ext(project_file)

    return os.path.splitext(_filename_ext)[1]


def projectfile_path(project_file):
    """Expects __file__.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/draw/
    """

    _projectfile_filepath = projectfile_fullpath(project_file)

    return os.path.split(_projectfile_filepath)[0]


def projectfile_folder(project_file):
    """The direct folder of __file__.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/draw/
    """

    _projectfile_folder = projectfile_path(project_file)
    return _projectfile_folder


def projectfile_apppath(project_file):
    """The python app folder of __file__.
    IE: The one below yaml.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/draw/
    """

    _known_path = projectfile_folder(project_file)

    while not _is_yaml_folder(os.path.split(_known_path)[0]):
        """Keep climbing up the known_path until you find the "yaml" file.
        Assumes your app folders are children of a folder with yaml.
        """
        _known_path = os.path.split(_known_path)[0]

    return _known_path


def projectfile_projectpath(project_file):
    """The python project folder of __file__.
    IE: Parent of `projectfile_apppath`.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/
    """

    _app_path = projectfile_apppath(project_file)
    return os.path.split(_app_path)[0]


def project_path():
    """The python project folder, whatever you are using.

    >> home/repo/drawing_app/draw/smart_draw.py
        >> home/repo/drawing_app/

    """

    return os.getcwd()
