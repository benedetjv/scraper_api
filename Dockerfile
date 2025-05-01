FROM python:3.11-slim

WORKDIR /app
COPY . .

# Instala Chrome e dependências
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    chromium chromium-driver \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "scraper_api:app", "--host", "0.0.0.0", "--port", "8080"]
