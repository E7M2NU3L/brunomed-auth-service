FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/* 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python /app/src/manage.py makemigrations && python /app/src/manage.py migrate && python /app/src/manage.py runserver 0.0.0.0:8000"]