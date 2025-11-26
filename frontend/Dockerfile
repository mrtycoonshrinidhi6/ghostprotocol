# ───────────────────────────────
# FRONTEND DOCKERFILE (Streamlit)
# ───────────────────────────────

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by Streamlit
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy frontend requirements
COPY frontend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all frontend files
COPY frontend/ .

# Default Streamlit port
ENV PORT=8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
