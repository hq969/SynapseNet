# Use a lightweight Python base image
FROM python:3.10-slim

# Prevent Python from writing pyc files and keep stdout unbuffered for logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the gRPC server code and protobufs
COPY ./communication/ ./communication/
COPY ./models/ ./models/
COPY ./main.py .

# Expose the standard gRPC port
EXPOSE 50051

# Create a non-root user for security best practices
RUN useradd -m synapse_user
USER synapse_user

# Start the gRPC service
CMD ["python", "main.py"]
