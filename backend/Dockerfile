# Use official Python image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Copy the entire project (NOT only the backend folder)
COPY . .

# Install backend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Cloud Run uses $PORT, so set default for local dev
ENV PORT=8000

# Start the backend
CMD ["python", "backend/api.py"]
