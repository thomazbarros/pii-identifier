#FROM python:latest
FROM --platform=linux/amd64 python:latest
RUN apt-get update && apt-get install -y mariadb-client

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD python -m uvicorn api :app --host 0.0.0.0 --port 80
CMD  python3 api/app.py