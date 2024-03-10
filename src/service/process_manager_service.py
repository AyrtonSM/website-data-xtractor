import threading


class ProcessManagerService:

    def run_threads(self, function: callable, data: dict, queue: any):

        thread_pool = []

        for page in data['contents']:
            function_args = (page['content'], page['url'], queue)
            thread = threading.Thread(target=function, args=function_args)
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()
