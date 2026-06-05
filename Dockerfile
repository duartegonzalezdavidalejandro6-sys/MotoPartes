FROM python:3.13-slim
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    pkg-config \
    gcc \
    build-essential \
    libcairo2-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "motopartesetings.wsgi:application", "--bind", "0.0.0.0:8080"]

