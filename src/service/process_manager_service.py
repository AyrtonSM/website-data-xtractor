
import threading
import requests as rq
class ProcessManagerService:

    def run_threads(self, function: callable, data: dict, queue: any, thread_count: int = 10):

        thread_pool = []

        for page in data['page_map']:
            url = page['url']
            content = page['content']

            function_args = (content, url, queue)
            thread = threading.Thread(target=function, args=function_args)
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()
