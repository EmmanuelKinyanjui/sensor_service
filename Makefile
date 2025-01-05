start-service:
	uvicorn core.main:app --reload

start-consumer:
	huey_consumer core.tasks.tasks.huey

test:
	ENV_FILE=.env.test pytest -vv --capture=no