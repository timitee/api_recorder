# -*- encoding: utf-8 -*-
import os


def _is_yaml_folder(known_path):
    """Utility: Reports whether the known_path has a setup.yaml file."""

    return os.path.exists(os.path.join(known_path, 'setup.yaml'))


def projectfile_fullpath(project_file):
    """Expects __file__."""

    return os.path.realpath(project_file)


def projectfile_path(project_file):
    """Expects __file__."""

    _projectfile_filepath = projectfile_fullpath(project_file)

    return os.path.split(_projectfile_filepath)[0]


def projectfile_filename_ext(project_file):
    """The filename and file extension."""

    _known_path = projectfile_fullpath(project_file)

    return os.path.split(_known_path)[1]


def projectfile_filename(project_file):
    """The name of the file without extension."""

    _filename_ext = projectfile_filename_ext(project_file)

    return os.path.splitext(_filename_ext)[0]


def projectfile_ext(project_file):
    """The file extension."""

    _filename_ext = projectfile_filename_ext(project_file)

    return os.path.splitext(_filename_ext)[1]


def projectfile_folder(project_file):
    """The direct folder of __file__."""

    _projectfile_folder = projectfile_path(project_file)
    return _projectfile_folder


def projectfile_apppath(project_file):
    """The python app folder of __file__.
    IE: The one below yaml.
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
    """

    _app_path = projectfile_apppath(project_file)
    return os.path.split(_app_path)[0]


def project_path():
    """The python project folder whatever you are using."""

    return os.getcwd()
