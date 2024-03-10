from queue import Queue
import threading as th
import requests as rq
from src.utils.logging_utils import *


class RequestService:

    def __init__(self):
        self._content_queue = Queue()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_multiple_url(self, urls: list) -> list:

        contents = []
        thread_pool = []
        for url in urls:
            function_args = (url, self._content_queue,)
            thread = th.Thread(target=self._fetch_content, args=function_args)
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()

        while not self._content_queue.empty():
            contents.append(self._content_queue.get())

        return contents

    def _fetch_content(self, url: str, queue: any):
        content = rq.get(url, headers=self._headers).text
        queue.put({
            'url': url,
            'content': content
        })
