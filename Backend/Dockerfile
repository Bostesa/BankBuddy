FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Ensure the entrypoint script is executable using its absolute path
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Use absolute path in ENTRYPOINT
ENTRYPOINT ["/app/entrypoint.sh"]
