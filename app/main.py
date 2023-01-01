import random
import time

import requests
from loguru import logger
from prometheus_client import Gauge, start_http_server

from config import (
    TELE2_URL,
    LOTS,
    MIN_SLEEP_SECONDS,
    MAX_SLEEP_SECONDS,
    MIN_SLEEP_MINUTES,
    MAX_SLEEP_MINUTES,
    HEADERS,
)


class Metrics:
    def __init__(self, lots):
        self.metrics = dict()
        self.lots = lots
        self.create_metrics()

    def create_metrics(self):
        for traffic_type, lots_sizes in self.lots.items():
            for lot_size in lots_sizes:
                if traffic_type not in self.metrics:
                    self.metrics[traffic_type] = dict()
                self.metrics[traffic_type][lot_size] = Gauge(
                    f"lots_{traffic_type}_{lot_size}", f"{traffic_type} {lot_size} lots"
                )


class Market:
    def __init__(self, url, headers):
        self.headers = headers
        self.url = url
        self.metrics = Metrics(LOTS)

    def update_metrics(self):
        logger.debug("start get_lots")

        for traffic_type in self.metrics.lots:
            logger.debug(traffic_type)
            time.sleep(random.randrange(1, 3))
            url = self.url + traffic_type

            lots = self.get_lots(url)
            for lot in lots:
                lot_name = int(lot["volume"])
                lot_counts = int(lot["count"])

                if lot_name in self.metrics.metrics[traffic_type]:
                    self.metrics.metrics[traffic_type][lot_name].set(lot_counts)
                    logger.info(f"{traffic_type} {lot_name}: {lot_counts}")

    def get_lots(self, url: str) -> dict:
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            sleep = random.randrange(MIN_SLEEP_MINUTES * 60, MAX_SLEEP_MINUTES * 60)
            logger.warning(f"status_code {response.status_code}. Sleep {sleep} seconds")
            time.sleep(sleep)
            return {}
        try:
            data = response.json()
        except Exception as e:
            logger.error(e)
            logger.error(response.content)
            sleep = random.randrange(MIN_SLEEP_MINUTES * 60, MAX_SLEEP_MINUTES * 60)
            logger.warning(f"status_code {response.status_code}. Sleep {sleep} seconds")
            time.sleep(sleep)
            return {}

        return data["data"]


if __name__ == "__main__":
    start_http_server(8000)
    market = Market(TELE2_URL, HEADERS)

    while True:
        market.update_metrics()
        sleep_time = random.randrange(MIN_SLEEP_SECONDS, MAX_SLEEP_SECONDS)
        logger.debug(f"sleep {sleep_time} seconds")
        time.sleep(sleep_time)
