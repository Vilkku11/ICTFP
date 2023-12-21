#DOCKERFILE

# Stage 1: initiate image and copy dependencies
FROM python:3.11-slim
WORKDIR /app
COPY venv/ /app
COPY frontend/dist /app/frontend/dist
COPY server/ /app
ENV PATH="/app/venv/bin:$PATH"