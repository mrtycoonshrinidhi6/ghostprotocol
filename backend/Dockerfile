# Use official Python image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements first (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the entire backend folder
COPY . .

# Expose port (Cloud Run expects the app to listen on PORT env variable)
ENV PORT=8080

# Command to run your backend
CMD ["python", "quick_start.py"]
