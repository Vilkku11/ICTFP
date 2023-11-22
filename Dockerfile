FROM python:3.9
WORKDIR /app
COPY . /app
ENV PATH="/app/venv/bin:$PATH"