# RSG Django Template - Django Project

RSG Django Template.

This document is primarily designed for technical staff working on the development of the project (e.g. software engineers and system admins).


## Django Project

The project is called 'django-template', but project files are stored in the 'core' folder. Please refer to `core/settings.py` for further details


## Django Apps

Apps include:

+ general - this is for static, general sections of the website (e.g. cookies page, accessibility page, etc.) that don't require a data model


## Django Admin

The provided Django Admin feature is utilised within this Django project, to allow the research project team to perform CRUD operations on the database using an intuitive web interface.


## Tests

There are a series of automated tests located in each Django app folder as 'tests.py'

To perform the tests:

+ Run: python manage.py test
+ Use the feedback given by Django for any failed tests to fix issues
+ Repeat this until returns a 100% pass rate


Once finished testing, remember to reverse the changes made to the project setup:

+ Delete any unwanted migrations in migrations folders
+ Delete the fixtures directory, including test.json fixture, for each app


This also complies with Flake8 for testing against PEP8:

+ Use pip install flake8 to install (if not already installed)
+ Run `flake8` to perform the tests
+ There's a `.flake8` file in the repo root directory, used to customise Flake8 tests


You can use coverage to see how much of the code is included in the tests:

+ Use `pip install coverage` to install (if not already installed)
+ Use the `.coveragerc file` to customise, e.g. to ignore particular folders, etc
+ Run: `coverage run manage.py test`
+ Run: `coverage html`
+ This should create a htmlcov folder. View the index.html page in this folder using a web browser


## JavaScript

+ JavaScript files are stored in `django/core/static/js`
+ For linting JavaScript, we recommend [eslint](https://eslint.org/) and include a `.eslintrc.json` config file in this repository
+ For testing JavaScript, we use [Jest](https://jestjs.io/). Each relevant JavaScript function has a corresponding test script that Jest will run by executing the command `npm run test`
+ For bundling JavaScript files, we use [Browserify](https://browserify.org/). Each time a change is made to the standard files (e.g. main.js or the individual functions) you must bundle these into `bundle.js`, which is then read by the browser. You can bundle by running, for example, `browserify main.js -o bundle.js'


## Accessibility

Our websites must comply with accessibility regulations. See the [BEAR Accessibility](https://accessibility.bear.bham.ac.uk/) site for more information.

Please note that the RSG's template Django project will link to the home page of the BEAR Accessibility website in the footer. This will likely need to be changed (on a per site basis) to the specific page that holds the correct accessibility statement for each site. E.g. standard CAL Django websites can point to: <https://accessibility.bear.bham.ac.uk/statements-cal.html> or you may need to create a new statement page and link to that.


## Database

The SQLite3 database used sits in the Django project root folder (alongside this README file). It is not included within the Git repo, so must instead be requested from the system admin. Once you have a copy of this database, give it a suitable name like `django-template.sqlite3` and place in the `django/` directory (same directory that stores `manage.py`). Remember to name this database in `local_settings.py` (see Settings section of this document for more details)


## Settings

There are 2 settings related files:

+ `settings.py` (for general project settings, regardless of environment and containing publicly accessible information)
+ `local_settings.py` (for settings specific to that environment (e.g. dev/test/production) and for private information (e.g. API keys))

`local_settings.py` is ignored from Git, as it contains private information that shouldn't be shared with others. Instead, the file `local_settings.example.py` is stored in Git to show you what information your own `local_settings.py` needs to contain. `local_settings.test.py` is used in the CI and should never be used on a production system. The steps you must take to configure `local_settings.py` are:

+ Create a `local_settings.py` file
+ Copy and paste the content from `local_settings.example.py` into `local_settings.py`
+ Customise this content by following the guide in `local_settings.example.py`
+ Do not delete or modify `local_settings.example.py`, as this will be kept in Git to help others
