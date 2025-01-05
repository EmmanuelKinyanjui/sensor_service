
# Sensor Data Service

A FastAPI-based service for processing and retrieving sensor data with time-series analytics capabilities.

## Features

- Receive encoded sensor data via POST endpoint
- Retrieve aggregated sensor data with flexible time intervals
- Background task processing for sensor data
- Time-series data aggregation with multiple interval options
- Sensor-specific data filtering

## API Endpoints

### POST /sensor_data/

Receives encoded sensor data and processes it asynchronously.

**Request Format:**

```json
{
    "message": {
        "attributes": {
            "key": "value"
        },
        "data": "base64_encoded_string",
        "messageId": "2070443601311540",
        "message_id": "2070443601311540",
        "publishTime": "2021-02-26T19:13:55.749Z",
        "publish_time": "2021-02-26T19:13:55.749Z"
    },
    "subscription": "projects/myproject/subscriptions/mysubscription"
}

```

### GET /sensor_data/

Retrieves aggregated sensor data with flexible filtering options.

## Query Parameters

- sensor_id (optional): Filter by specific sensor
- start_time (optional): Start timestamp for data range
- end_time (optional): End timestamp for data range
- interval: Aggregation interval (minute, hour, day, week, month)

## Response Format

```json
{
    "chart_data": {
        "timestamps": ["2023-01-01T00:00:00"],
        "presence": [0.75],
        "dwell_time": [120.5],
        "reading_count": [42]
    }
}
```

### Dependencies

- Poetry for dependency management
- Python 3.x
- FastAPI
- SQLAlchemy (via alembic)
- Postgresql (configured via SQLAlchemy)
- Redis (for background task processing)

## How to run the project

### Environment variables

I use `.env` files to store environment variables that will be accessed within the application.

Copy the `.env.sample` to `.env` by running:

```shell
cp .env.sample .env
```

Update the variables in the `.env` file to suit your setup before proceeding to the next steps


### Create a database

Create a database in Postgresql named `sensor_data`

### Activate virtual environment

```shell
poetry shell
```

This will activate a virtual environment that is specific to your project. If none exists, it will create and initialize one

### Install dependencies

```shell
poetry install
```

This will install all dependencies in the virtual environment

### Run database migrations

Run project migrations with the command

```shell
alembic upgrade head
```

### Start backend app in dev mode

```shell
make start-service 
```

This will start the application on port `8000`

```shell
make start-consumer
```

This will start the background task

## Testing

To run tests copy the `.env.sample` file to a `.env.test`. Update the environment variables for your tests and run the command

```shell
ENV_FILE=.env.test pytest -vv --capture=no
```

If the `ENV_FILE` is not provided, it defaults to using the `.env` file if one exists

> **Note:** The database url `DATABASE_URL` does not need to be an existing database. If it does not exist, it will be created automatically and dropped once the tests have completed.

> **Note:** A Makefile has been provided to simplify running the commands above.

## Documentation

| Environment | Links                                                                                                             |
|:------------|:------------------------------------------------------------------------------------------------------------------|
| Local       | [Swagger](http://localhost:8000/docs/), [ReDoc](http://localhost:8000/redoc)                                      |
