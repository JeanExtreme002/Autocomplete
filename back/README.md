# Back-end
This is the back-end server of the auto complete project.

## Getting Started

First, make sure Elasticsearch is alive and `.env` file is configured. 

Install the dependencies for the project:
```
$ pip install poetry
$ poetry install
```

Now, you can run the server with:
```
$ poetry run python -m src
```

Populate the application by running the following command:
```
$ poetry run python -m src.seeder
```

## Running tests
The back-end has some tests to check if everything is working properly. To run the tests, execute the command below:
```
$ poetry run python -m unittest discover -s tests --verbose
```