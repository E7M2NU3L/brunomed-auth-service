FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "/app/src/manage.py", "runserver" ]