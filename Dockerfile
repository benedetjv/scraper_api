FROM python:3.11-slim

# Instalações essenciais para selenium + chrome
RUN apt-get update && apt-get install -y \
    chromium-driver chromium unzip curl wget gnupg \
    && apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "scraper_api:app", "--host", "0.0.0.0", "--port", "8080"]
