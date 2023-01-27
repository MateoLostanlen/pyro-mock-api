# this target runs checks on all files and potentially modifies some of them
style:
	isort .
	black .

# Run the docker
run:
	uvicorn main:app --reload
