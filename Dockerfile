# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to ensure Python output is sent straight to the terminal (e.g., logs)
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port on which the application will run
EXPOSE 8010
RUN chmod +x /usr/local/bin/uvicorn
# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "4"]
