import os
import json

TELE2_URL = os.getenv(
    "URL", "https://tele2.ru/api/exchange/lots/stats/volumes?trafficType="
)

LOTS = json.loads(os.getenv("LOTS", '{"data": [5, 6], "voice": [50, 200, 201, 202]}'))

MIN_SLEEP_SECONDS = int(os.getenv("MIN_SLEEP_SECONDS", 55))
MAX_SLEEP_SECONDS = int(os.getenv("MAX_SLEEP_SECONDS", 80))

MIN_SLEEP_MINUTES = int(os.getenv("MIN_SLEEP_MINUTES", 5))
MAX_SLEEP_MINUTES = int(os.getenv("MAX_SLEEP_MINUTES", 10))

HEADERS = {
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}