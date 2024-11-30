FROM python:3.9-slim  

WORKDIR /app  

COPY backup.py config.ini /app/ 

RUN pip install -r requirements.txt || 

CMD ["python", "backup.py"] 
