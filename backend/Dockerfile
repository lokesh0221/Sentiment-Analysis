# backend/Dockerfile

### Stage 1 — Build layer
FROM python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir /app/export && \
    cp -r /root/.local /app/export/.local && \
    cp -r . /app/export

### Stage 2 — Runtime
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app/export /app

ENV PATH="/app/.local/bin:$PATH"
ENV PYTHONPATH="/app"

# 👇 Make finetune.py executable in container
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
