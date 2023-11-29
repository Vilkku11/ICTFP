FROM python:3.11-slim
WORKDIR /app
COPY . /app
ENV PATH="/app/venv/bin:$PATH"