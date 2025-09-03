FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential     && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
 
COPY app /app/app

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --retries=10 CMD curl -f http://localhost:8000/health || exit 1

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
