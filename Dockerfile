# Lightweight Python runtime for the hello.py UAT application and its test.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install all dependencies (app + monitoring)
COPY requirements.txt requirements-monitoring.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt -r requirements-monitoring.txt

COPY hello.py test_hello.py monitor.py ./

# Default container action: run the app. Tests can override CMD at docker run time.
CMD ["python", "hello.py"]
