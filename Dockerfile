FROM python:3.9-slim-buster

RUN pip install speedtest-cli influxdb-client toml

WORKDIR /app
COPY script.py /app

CMD ["python", "script.py"]
