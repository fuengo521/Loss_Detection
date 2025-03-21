# Define the virtual env
VENV = venv 
PYTHON = $(VENV)/bin/python 

setup:
	python setup.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Docker Commands
docker-build:
	docker build -t my_project_image .

docker-run:
	docker run -p 5000:5000 my_project_image

docker-stop:
	docker stop $$(docker ps -q)

docker-clean:
	docker system prune -af
