This project might not a boilerplate, but you can find an example how to build small-to-medium (or maybe even large) scale flask-based application with few cases that might be needed further on you development process.

I ran this template for one of startup company in Indonesia and able to serve millions request per day.

You can implement Monorepo for multiple python-based projects with this schema, why? Facebook/Google uses a giant monorepo for their billions line of code and you can find another benefit using Monorepo at: https://gomonorepo.org/


### Getting Started

------------------------------------------------------------------------

##### 1. Virtual Environment 
First, I'd recommend you to use Virtual Env and install the necessary package specifically only used by ts project:
```sh
$ virtualenv venv; 
$ source venv/bin/activate 
(env) $ pip install -r requirements.txt
```

##### 2. Setup The Database
Then create a new database, we're using Postgresql here as an example.
```sh
postgres=# CREATE USER admin WITH PASSWORD 'password';
postgres=# CREATE DATABASE marketplace;
postgres=# GRANT ALL PRIVILEGES ON DATABASE marketplace TO admin;
```

##### 3. Migrate The Database Model
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

##### 4. Run The Unit Test
Writing proper Unit Test is one of important keys delivering clean working product, 
so here they are in Flask, you should NOT ignore this one before committing the code.
```sh
(env) $ python manage.py test
```

##### 5. Flake8: Your Tool For Code Style Guide Enforcement
Flake8 is a code style checker - _to beautify your code (and more readable!)_ - that can be integrated into your CI.
```sh
(env) $ flake8 path/to/code/to/check.py
```
or just type on your root project folder, it will read *setup.cfg* file
```sh
(env) $ flake8
```

##### 6. Run The Server
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

##### 6. Flask-Swagger 

Swagger pages will automatically loaded and shown as your registered blueprint's version e.g. v1, v2 etc.
 
Check and Test APIs through Swagger [HERE](http://localhost:5000/api/v1/swagger).


Before Testing the APIs, please run this command to create a new User as `John Doe`
```sh
(env) $ python manage.py initdb
```

Test new user `John Doe` by using this bash shell command
```sh
(env) $ curl -X POST "http://localhost:5000/api/v1/user/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"john_doe_1946\", \"password\": \"this15secret\"}"
```

Expected will return a response as
```
{
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTU1MjEyMTc1NiwiZXhwIjoxNTU0NTQwOTU2fQ.eyJzZXNzaW9uX2lkIjoiNmM1MzY2MDkiLCJ1c2VybmFtZSI6ImpvaG5fZG9lXzE5NDYifQ.TvQn76Ek7sPCLHS4hxMuk3XuQzvOt_pWL5w3_I84mvc",
  "username": "john_doe_1946"
}
```

---


Further Info? Contact me at [Linkedin](https://www.linkedin.com/in/dandi-diputra/)
