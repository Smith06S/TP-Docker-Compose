FROM python:3.12

WORKDIR /server

RUN pip install --no-cache-dir mysql-connector-python fastapi uvicorn pymongo

COPY main.py /server/main.py

EXPOSE 8000