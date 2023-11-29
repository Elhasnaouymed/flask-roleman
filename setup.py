from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.0'
DESCRIPTION = 'Flask Extension for User Authorizations, Users can have Groups, and Each Group can have Roles, more control and easy to use.'

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Setting up
setup(
    name="flask-roleman",
    version=VERSION,
    author="Mohamed El-Hasnaouy",
    author_email="<elhasnaouymed@proton.me>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['flask', 'flask_login', 'flask_sqlalchemy'],
    keywords=['flask', 'extension', 'roles', 'authorization', 'permissions', 'security', 'groups', 'privileges'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ]
)
