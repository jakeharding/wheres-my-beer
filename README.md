# CSCI4970 - Capstone project Spring 2018

## Draught picks - A beer profiling and recommendation application

Dev Branch Status:
[![Coverage Status](https://coveralls.io/repos/github/jakeharding/draught-picks-backend/badge.svg?branch=dev)](https://coveralls.io/github/jakeharding/draught-picks-backend?branch=dev)

Please see the [contributing](https://github.com/jakeharding/draught-picks-backend/master/CONTRIBUTING.md) document for contribution guidelines.

## Backend

The backend consists of a Django web application.  
A virtualenv using Python 3.6 is recommended in order to isolate Python dependencies.
PostgreSQL is used for a database system. Database settings will need to configured in a local_settings.py file, and
the postgres service will need to be running.
An example local settings file [here](https://github.com/jakeharding/draught-picks-backend/master/draught_picks/draught_picks/local_settings.py.example).
Installing Python and any database system is platform dependent.

[comment]: <> (A Redis server not currently needed)
[comment]: <> (
A Redis server is necessary to run the application.
Make sure that your Redis server is running on port 6379.
Installing Redis is platform dependent.   )

To install Python dependencies run `pip install -r requirements.txt`.
After Python requirements are installed and the database is created, migration will need to be ran to create tables in the database.
To run the migrations run `python manage.py migrate`.
To run the Django development server run `python manage.py runserver`.

Open a browser to `http://localhost:8000`.
