# Dockerfile
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y python3-dev libgpiod2 python3-rpi.gpio spidev

# Copy application files
WORKDIR /app
COPY . /app

# Install Python packages
RUN pip install -r requirements.txt

# Expose the application's port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
