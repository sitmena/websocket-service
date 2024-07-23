# Define the image name
IMAGE_NAME = websocket-service

# Command to build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Command to run the Docker container
run:


# Command to stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Command to stop, remove, and run the Docker container
restart: stop run

# Command to remove the Docker image
clean:
	docker rmi $(IMAGE_NAME) || true

# Command to list all Docker containers (optional)
list-containers:
	docker ps -a

# Command to list all Docker images (optional)
list-images:
	docker images
