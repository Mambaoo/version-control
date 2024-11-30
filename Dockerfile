FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt #fix error

COPY backup.py config.ini /app/

CMD ["python", "backup.py"]
