FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY filesystem_pipeline.py .

COPY /data /app/data

CMD ["python", "filesystem_pipeline.py"]
