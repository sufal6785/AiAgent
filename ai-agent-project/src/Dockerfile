FROM ubuntu:latest

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv g++ openjdk-11-jdk docker.io bash && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create virtual environment
RUN python3 -m venv /app/venv

# Copy API server files and requirements.txt
COPY server.py /app/
COPY requirements.txt /app/

# Install Python dependencies in the virtual environment
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Use virtual environment for execution
CMD ["/app/venv/bin/python", "server.py"]
