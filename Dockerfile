# Lightweight Python runtime for the hello.py UAT application and its test.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only essential dependencies (just pytest)
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY hello.py test_hello.py ./

# Default container action: run the app. Tests can override CMD at docker run time.
CMD ["python", "hello.py"]
