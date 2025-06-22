# File: messaging_app/Dockerfile

FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY .. /app

# For 'docker run', use -p 8000:8000 to map this port.
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]