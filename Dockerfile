# ============================
# Stage 1: Build dependencies
# ============================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system deps (for httpx / OpenAI)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ============================
# Stage 2: Runtime container
# ============================
FROM python:3.11-slim

WORKDIR /app

# Copy installed deps from builder
COPY --from=builder /root/.local /root/.local

# Add pip packages to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy source code
COPY app/ app/
COPY frontend/ frontend/
COPY requirements.txt .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
