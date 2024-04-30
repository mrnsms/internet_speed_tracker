import time
import toml
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from speedtest import Speedtest

def internet_speed_test():
    speed_test = Speedtest()
    best_server = speed_test.get_best_server()  # Fetches best server based on ping
    download_speed = speed_test.download() / 1_000_000  # Convert to Mbps
    upload_speed = speed_test.upload() / 1_000_000  # Convert to Mbps
    ping = best_server['latency']  # Latency in ms
    jitter = speed_test.results.ping_variance  # Jitter in ms
    return download_speed, upload_speed, ping, jitter

def log_to_influxdb(client, bucket, org, download, upload, ping, jitter):
    point = Point("internet_speed")
        .tag("unit", "Mbps")
        .field("download", download)
        .field("upload", upload)
        .field("ping", ping)
        .tag("latency_unit", "ms")
        .field("jitter", jitter)
        .tag("jitter_unit", "ms")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=bucket, org=org, record=point)

def main():
    config = toml.loads('<config_toml>')  # Load config from a TOML string provided at runtime
    interval = config['settings']['interval_minutes']
    influxdb_url = config['settings']['influxdb_url']
    token = config['settings']['token']
    org = config['settings']['org']
    bucket = config['settings']['bucket']

    client = InfluxDBClient(url=influxdb_url, token=token, org=org)
    while True:
        download, upload, ping, jitter = internet_speed_test()
        log_to_influxdb(client, bucket, org, download, upload, ping, jitter)
        time.sleep(interval * 60)

if __name__ == "__main__":
    main()
