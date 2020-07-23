
import unittest
from setuptools import setup
try: # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession


################################################################################
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('argoslabs.mygroup.mycalc',
                                      pattern='test*.py')
    return test_suite


################################################################################
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("argoslabs\\mygroup\\mycalc\\requirements.txt", session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]
reqs.extend([])

setup(
    name='argoslabs.mygroup.mycalc',
    test_suite='setup.my_test_suite',
    packages=[
        'argoslabs','argoslabs.mygroup','argoslabs.mygroup.mycalc','argoslabs.mygroup.mycalc.tests'
    ],
    version='2.602.2002',
    description='ARGOS-LABS RPA plugin module sample',
    author='Jerry Chae',
    author_email='mcchae@argos-labs.com',
    url='https://www.argos-labs.com',
    license='ARGOS-LABS Proprietary License',
    keywords=['rpa', 'robot', 'module', 'mygroup', 'mycalc', 'argoslabs'],
    platforms=['Mac', 'Windows', 'Linux'],
    install_requires=reqs,
    python_requires='>=3.6',
    package_data={'argoslabs.mygroup.mycalc': ['icon.*', 'dumpspec.json']},
    zip_safe=False,
    classifiers=[
        'Build :: Date :: 2020-07-23 10:19',
        'Build :: Method :: alabs.ppm',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Change :: Log :: Unittest for Linux',
        'Topic :: Change :: Log :: Unittest for Mac',
        'Topic :: Change :: Log :: Unittest for Windows',
        'Topic :: Demo :: HelloWorld',
        'Topic :: RPA',
    ],
    entry_points={
        'console_scripts': [
            'argoslabs.mygroup.mycalc=argoslabs.mygroup.mycalc:main',
        ],
    },
    include_package_data=True,
)
