# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the main app
CMD ["python", "main.py"]
