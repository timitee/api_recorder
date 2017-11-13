import os
from distutils.core import setup


def read_file_into_string(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_readme():
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file_into_string(name)
    return ''


setup(
    name='api_recorder',
    packages=[
                'example_api_recorder',
                'example_api_recorder.tests',
                'api_recorder',
                'api_recorder.api_recorder',
                'api_recorder.api_recorder.tests',
                ],
    package_data={},
    version='0.0.1',
    description='api_recorder',
    author='Tim Bushell',
    author_email='tcbushell@gmail.com',
    url='git@github.com:timitee/api_recorder.git',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 1.10',
        'Topic :: Development :: API',
    ],
    long_description=get_readme(),
)
