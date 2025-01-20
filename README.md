[![Docker](https://github.com/dydanz/flask-boilerplate/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dydanz/flask-boilerplate/actions/workflows/docker-publish.yml)
[![Python CI](https://github.com/dydanz/flask-boilerplate/actions/workflows/python-app.yml/badge.svg)](https://github.com/dydanz/flask-boilerplate/actions/workflows/python-app.yml)

This project provides a template for building small-to-medium scale Flask applications with production-ready features. It has been proven to handle millions of requests per day in production environments.

### Getting Started

------------------------------------------------------------------------

#### Option A: Using Docker (Recommended)

1. **Build and Run with Docker Compose**
```sh
# Build and start the containers
$ docker-compose up --build

# Run in detached mode (optional)
$ docker-compose up -d
```

2. **Run Database Migrations**
```sh
# Run migrations inside the container
$ docker-compose exec web flask db upgrade

# Initialize test user
$ docker-compose exec web flask init-db
```

3. **Access the Application**
- Web Application: http://localhost:5001
- API Documentation: http://localhost:5001/api/v1/swagger

4. **Useful Docker Commands**
```sh
# View logs
$ docker-compose logs -f

# Stop the containers
$ docker-compose down

# Stop and remove volumes (clean slate)
$ docker-compose down -v

# Run tests
$ docker-compose exec web pytest

# Run code quality checks
$ docker-compose exec web flake8
$ docker-compose exec web black .
$ docker-compose exec web isort .
```

#### Option B: Local Development

1. Virtual Environment 
It's recommended to use a virtual environment. Modern Python projects often use `venv` (built into Python 3) or `poetry` for dependency management:

```sh
# Using venv (recommended for Python 3)
$ python -m venv venv
$ source venv/bin/activate 
(venv) $ pip install -r requirements.txt

# Alternative: Using Poetry (modern dependency management)
$ poetry install
```

2. Setup The Database
Create a new PostgreSQL database:
```sh
postgres=# CREATE USER postgres WITH PASSWORD 'postgres';
postgres=# CREATE DATABASE flask_marketplace;
postgres=# GRANT ALL PRIVILEGES ON DATABASE flask_marketplace TO postgres;
```

3. Database Migrations
We use Alembic for database migrations. While the commands below still work, modern Flask projects often use Flask-Migrate (which wraps Alembic):

```sh
# Modern approach using Flask-Migrate
(venv) $ flask db init
(venv) $ flask db migrate
(venv) $ flask db upgrade

# Legacy approach (still works)
(venv) $ python db migrate init
(venv) $ python db migrate migrate
(venv) $ python db migrate upgrade

#if you want to hard-reset the database (all data will be lost)
- Drop all tables on the database, then execute the following command
(venv) $ rm -rf migrations/
(venv) $ flask db init
(venv) $ flask db migrate -m "Initial migration with all models"
(venv) $ flask db upgrade
```

4. Testing
For modern Flask testing, we recommend pytest along with the traditional unittest:
```sh
# Using pytest (recommended)
(venv) $ pytest

# Legacy approach
(venv) $ python manage.py test
```

5. Code Quality Tools
Modern Python projects use multiple tools for code quality:
```sh
# Flake8 for style checking
(venv) $ flake8

# Black for code formatting (recommended)
(venv) $ black .

# isort for import sorting (recommended)
(venv) $ isort .

# mypy for type checking (recommended)
(venv) $ mypy .
```

6. Running the Server
Development server options:
```sh
# Modern Flask CLI approach (recommended)
(venv) $ export FLASK_APP=manage.py
(venv) $ export FLASK_ENV=development  # FLASK_CONFIG is legacy
(venv) $ flask run

# Legacy approach (still works)
(venv) $ python manage.py runserver

# Production WSGI server
# Note: Consider using uvicorn or hypercorn for ASGI support
(venv) $ gunicorn --bind 0.0.0.0:5000 manage:app -w 4 --timeout 180
```

7. API Documentation
Modern API documentation options:

- Flask-RESTX (recommended): Swagger/OpenAPI documentation with interactive UI
- Flask-Smorest: Modern OpenAPI documentation with marshmallow integration
- Legacy Flask-Swagger (deprecated): Basic Swagger support

Access the API documentation at: http://localhost:5000/api/v1/swagger

8. Authentication Example
Create a test user:
```sh
(venv) $ flask init-db  # Modern CLI approach
# or
(venv) $ python manage.py initdb  # Legacy approach
```

Test authentication:
```sh
$ curl -X POST "http://localhost:5000/api/v1/user/auth/login" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe_1946", "password": "this15secret"}'
```

Expected response:
```json
{
  "token": "eyJhbGciOiJIUzI1...",
  "username": "john_doe_1946"
}
```

---

### Recommended Modern Updates:

1. **Dependencies**: Consider using Poetry for dependency management
2. **Type Hints**: Add Python type hints throughout the codebase
3. **API Framework**: Consider migrating to Flask-RESTX or Flask-Smorest
4. **Authentication**: Consider using Flask-JWT-Extended for JWT handling
5. **Testing**: Add pytest with pytest-flask
6. **Documentation**: Use modern OpenAPI 3.0 specifications
7. **Async Support**: Consider adding ASGI support with Quart or async Flask

For questions or professional inquiries: [Linkedin](https://www.linkedin.com/in/dandi-diputra/)
