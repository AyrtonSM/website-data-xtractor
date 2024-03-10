from src.service.process_manager_service import ProcessManagerService
from src.service.request_service import RequestService
from src.service.image_service import ImageService
from src.service.phone_service import PhoneService
from src.utils.string_utils import *
import multiprocessing as mp
import json
import logging as logger

class XTractorService:

    def __init__(self, urls: list):
        self._queue = mp.Queue()
        self._image_service = ImageService()
        self._phone_service = PhoneService()
        self._function_definitions = [
            self._image_service.retrieve_logo_parallel,
            self._phone_service.retrieve_phones_parallel
        ]

        _processes_limit = len(self._function_definitions)
        _partition_size = int(len(urls) / _processes_limit) + 1
        self._urls_partitioned = [urls[i * _partition_size: (i + 1) * _partition_size] for i in range(_processes_limit)]
        if len(self._urls_partitioned[-1]) == 0:
            self._urls_partitioned = self._urls_partitioned[:-1]

    def extract(self, export_to_json: bool = True, filename: str = 'websites_logo_phone_extraction.json'):
        websites_information = self._extract_websites_information()
        websites_information = self._join_common_data_by_website_url(websites_information)

        if export_to_json:
            if not is_non_null_nor_empty(filename):
                filename = 'websites_logo_phone_extraction.json'
                logger.warning('File name is null or empty, using default name instead')

            path = f'files_output/json/{filename}'
            with open(path, 'w') as file:
                file.writelines(json.dumps(websites_information, indent=4))
                logger.info('Data extraction saved at %s', path)

        return websites_information

    @staticmethod
    def _join_common_data_by_website_url(websites_information: list) -> list:
        updated_attrs = []
        site_val = {}
        for info in websites_information:
            key = list(info.keys())[0]
            value = list(info.values())[0]

            if key not in site_val:
                site_val[key] = value
            else:
                for k, v in value.items():
                    existing_mapping = site_val[key]
                    if k not in existing_mapping:
                        site_val[key].update({k: v})
        for v in site_val.values():
            updated_attrs.append(v)

        return updated_attrs

    def _extract_websites_information(self) -> list:
        processes = []
        process_manager_service = ProcessManagerService()
        request_service = RequestService()
        for partition in self._urls_partitioned:
            contents = request_service.fetch_multiple_url(partition)
            for function_def in self._function_definitions:
                args = (function_def, {'contents': contents}, self._queue, )
                process = mp.Process(target=process_manager_service.run_threads, args=args)
                processes.append(process)
                process.start()
        for process in processes:
            process.join()

        websites_information = []
        while not self._queue.empty():
            websites_information.append(self._queue.get())

        return websites_information
