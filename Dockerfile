FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir . && playwright install --with-deps chromium
ENTRYPOINT ["python", "-m", "esidif_crawler"]
