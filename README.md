# Worker shift scheduling app

## Goal
Create an application that csan be used to schedule worker shifts.

## Prerequisites
- python3
- Django
- Postgres

### Run application
- Install all dependencies with `pip install requirements.txt`
- Set up your enviroment with the database credentials
        ENGINE=django.db.backends.postgresql
        DB_NAME=db
        DB_USERNAME=postgres
        DB_PASSWORD=postgres
        DB_HOST=localhost
- Make migrations with `python3 manage.py makemigrations`
- Run migrations with `python3 manage.py migrate` to create the tables
- Run the application with `python3 manage.py runserver`
- Run tests using `pytest`
- Documentation can be found at `http://127.0.0.1:8000/api/schema/redoc`

### Pending work
- Dockerize the application
- Deploy the application
- Improve the documentation
- Add linting with `eslint`
- Add a job that runs daily to complete all overdue shifts that are not completed
- Add functionality to create reports showing the hours a worker logged during a certain period

