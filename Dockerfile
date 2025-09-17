# ============================
# Stage 1: Build dependencies
# ============================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# ============================
# Stage 2: Runtime container
# ============================
FROM python:3.11-slim

WORKDIR /app

# Copy installed deps from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy only necessary code
COPY app/ app/
COPY frontend/ frontend/

# Expose FastAPI port
EXPOSE 8000

# Add healthcheck (optional, orgs love this)
HEALTHCHECK CMD curl --fail http://localhost:8000/weather?lat=0&lon=0 || exit 1

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
