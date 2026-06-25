# Stage 1 — build React frontend
FROM node:20-slim AS frontend
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2 — Python runtime
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=frontend /app/dist ./dist

RUN pip install --no-cache-dir -e .
RUN fc-cache -fv

EXPOSE 8000
CMD ["uvicorn", "api.orders:app", "--host", "0.0.0.0", "--port", "8000"]
