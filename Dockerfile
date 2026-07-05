FROM python:3.9-slim-buster

RUN apt-get update -y && \
    apt-get install -y awscli && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade accelerate transformers

COPY . /app

EXPOSE 8080

CMD ["python3", "app.py"]