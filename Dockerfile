FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY docker_monitor.py .

# Run the application
CMD ["python", "docker_monitor.py"]
