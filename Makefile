# Define the image name
IMAGE_NAME = doroob20docker/websocket-service

# Command to build the Docker image
build:
	docker buildx build --platform linux/amd64 -t $(IMAGE_NAME):14 .

# Command to run the Docker container
run:
	docker-compose up -d

# Command to stop and remove the Docker container
stop:
	docker-compose down

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
