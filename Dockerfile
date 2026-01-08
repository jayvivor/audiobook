# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY src/python/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY src/python/ .

# Command to run the application
CMD ["python", "main.py"]

version: '3.8'

services:
    audiobook:
        build:
            context: .
            dockerfile: Dockerfile
        container_name: audiobook_container
        stdin_open: true
        tty: true
        command: /bin/bash