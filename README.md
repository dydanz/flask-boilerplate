This project might not a boilerplate, but you can find an example how to build small-to-medium (or maybe even large) scale flask-based application with few cases that might be needed further on you development process.

I ran this template for one of startup company in Indonesia and able to serve millions request per day.


### Getting Started

------------------------------------------------------------------------

##### Virtual Environment 
First, I'd recommend you to use Virtual Env and install the necessary package specifically only used by ts project:
```sh
$ virtualenv venv; 
$ source venv/bin/activate 
(env) $ pip install -r requirements.txt
```

##### Setup The Database
Then create a new database, we're using Postgresql here as an example.
```sh
postgres=# CREATE USER admin WITH PASSWORD 'password';
postgres=# CREATE DATABASE marketplace;
postgres=# GRANT ALL PRIVILEGES ON DATABASE marketplace TO admin;
```

##### Migrate The Database Model
As you can find database model on the application, firstly you should init the alembic folder, generate a migration script and upgrade (commit database model changes) into your DBMS.

This kind of operation should be done if you have changes on your database model/schema. Otherwise, SQLAlchemy unable correctly data model mapping between you model-app-code and actual table on DBMS.

Create Alembic Versioning table on your db and folders on you project
```sh
(env) $ python db migrate init
```
Generate Migration Script
```sh
(env) $ python db migrate migrate
```
Apply the DB Model Changes
```sh
(env) $ python db migrate upgrade
```

##### Run The Unit Test
Writing proper Unit Test is one of important keys delivering clean working product, 
so here they are in Flask, you should NOT ignore this one before committing the code.
```sh
(env) $ python manage.py test
```

##### Flake8: Your Tool For Code Style Guide Enforcement
Flake8 is a code style checker - _to beautify your code (and more readable!)_ - that can be integrated into your CI.
```sh
(env) $ flake8 path/to/code/to/check.py
```
or just type on your root project folder, it will read *setup.cfg* file
```sh
(env) $ flake8
```

##### Run The Server
You can setup and use IDE or use terminal console to run the server locally, with your virtual-environment activated:
```sh
(env) $ export FLASK_APP=manage.py;
(env) $ export FLASK_CONFIG=development;
(env) $ flask run
```
.. or as an alternative:
```sh
(env) $ python manage.py runserver
```
.. or use to enable *gunicorn* or similar lightweight web server gateway interface (WSGI).
```sh
(env) $ gunicorn --bind 0.0.0.0:5000 manage:app -w 4 --timeout 180
```

By default Local Server will run on **http://localhost:5000** make sure the port not already in use.

Flask-Swagger will automatically loaded and shown as your registered blueprint's version e.g. v1, v2 etc.
 
Check and Test APIs through Swagger at **http://localhost:5000/api/v1/swagger**



---



Further Info? Contact me at [Linkedin](https://www.linkedin.com/in/dandi-diputra/)