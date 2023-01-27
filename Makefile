# this target runs checks on all files and potentially modifies some of them
style:
	isort .
	black .

# Run the docker
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
