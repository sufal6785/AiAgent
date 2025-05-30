FROM ubuntu:latest

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get install -y g++ openjdk-11-jdk docker.io bash

# Set working directory
WORKDIR /app

# Create virtual environment and install dependencies
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install flask flask-cors flask-jwt-extended bcrypt

# Copy API server files
COPY server.py /app/

# Use virtual environment for execution
CMD ["venv/bin/python", "server.py"]
