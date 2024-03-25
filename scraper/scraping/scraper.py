from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

from fake_useragent import UserAgent
import requests

import logging
logger = logging.getLogger(__name__)

class Scraper:
    def __init__(self, n_tries=3, n_threads=10, wait_time_min=0.1, wait_time_max=1.0):
        self.n_tries = n_tries
        self.n_threads = n_threads
        self.ua = UserAgent(platforms="pc")

    def fetch(self, url):
        for i in range(self.n_tries):
            try:
                time.sleep(random.uniform(0.1, 1.0))
                resp = requests.get(url, headers={'User-Agent': self.ua.random})
                assert resp.status_code == 200
                return resp
            except Exception as e:
                # print(f"Attempt {i+1} failed for URL: {url}. Error: {str(e)}. Status code: {resp.status_code}")
                pass
        print(f'Failed to fetch {url}, status code: {resp.status_code}')

    def fetch_multiple(self, urls):
        with ThreadPoolExecutor(max_workers=self.n_threads) as executor:
            future_to_url = {executor.submit(self.fetch, url): url for url in urls}
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    yield url, data
                except Exception as e:
                    logger.error(f"Failed to fetch {url} with error: {e}")
                    yield None, None