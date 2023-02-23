from setuptools import setup

long_description = None

with open("README.md", 'r') as fp:
    long_description = fp.read()

setup(
    name = 'pyBlaubergAHU',
    packages = ['blaubergahu'],
    version='0.1.0',
    description='Python3 library for Blauberg Komfort AHU',
    long_description=long_description,
    python_requires='>=3.6.7',
    author='Tim Welch',
    author_email='tim.welch.nz@gmail.com',
    url='https://github.com/timwelchnz/pyBlaubergAHU',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
)
