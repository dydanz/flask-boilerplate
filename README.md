First, setup virtual environment and install the necessary package:
------------------------------------------------------------------------
```sh
$ virtualenv venv; source venv/bin/activate; pip install -r requirements.txt
```


## To setup Postgresql database:
------------------------------------------------------------------------
```sh
postgres=# CREATE USER admin WITH PASSWORD 'password';
postgres=# CREATE DATABASE marketplace;
postgres=# GRANT ALL PRIVILEGES ON DATABASE marketplace TO admin;
```


To run the server with your virtual-environment activated:
------------------------------------------------------------------------
```sh
$ export FLASK_APP=manage.py;
$ export FLASK_CONFIG=development;
$ flask run
```
or as an alternative:
```sh
$ python manage.py runserver
```
or use to enable *gunicorn* or similar lightweight web server gateway interface (WSGI).
```sh
$ gunicorn --bind 0.0.0.0:5000 manage:app -w 4 --timeout 180
```