URL_MAP = {}



# import threading
# # from queue import Queue
#
#
# class SingletonDataContextManager:
#
#     URL_MAP: dict = {}
#     # _instance = {}
#     _lock = threading.Lock()
#
#     @classmethod
#     def add_to_url_map(cls, data: dict):
#         with cls._lock:
#             if not cls.URL_MAP:
#                 cls.URL_MAP = {}
#             cls.URL_MAP.update(data)
#             print(cls.URL_MAP)
#
#     @classmethod
#     def get_url_map(cls):
#         with cls._lock:
#             if not cls.URL_MAP:
#                 cls.URL_MAP = {}
#                 return cls.URL_MAP
#
#             return cls.URL_MAP
#
#     @classmethod
#     def get_instance(cls):
#         return cls


    #
    # def __new__(cls, *args, **kwargs):
    #     print('->', cls._instance, args, kwargs)
    #     if not cls._instance:
    #         with cls._lock:
    #             if not cls._instance:
    #                 # cls._queue = Queue()
    #                 cls._instance = super().__new__(cls, *args, **kwargs)
    #
    #     return cls._instance
    #
    # # def get_queue(self):
    # #     return self._queue
