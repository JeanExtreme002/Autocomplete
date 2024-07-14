# Back-end
This is the back-end server of the auto complete project.

## Getting Started

First, make sure Elasticsearch is running and `.env` file is configured. 

Install the dependencies for the project:
```
$ pip install poetry
$ poetry install --with dev
```

Now, you can run the server with:
```
$ poetry run python -m src
```

Populate the application by running the following command:
```
$ poetry run python -m src.seeder
```

## Running Tests
The back-end has some tests to check if everything is working properly. To run the tests, execute the command below:
```
$ poetry run python -m unittest discover -s tests --verbose
```

## Coding Style
Run the commands below to properly format the project's code:
```
$ poetry run flake8 .
$ poetry run black .
```
