# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
# Adjusted for build context at project root
COPY backend/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# We copy everything from root to /app so that imports like 'from agents_realtime import ...' work
COPY . .

# Expose port 8000
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME=backend.api
ENV VARIABLE_NAME=app
ENV PORT=8000
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
