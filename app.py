import sys

from src.service.image_service import ImageService
from src.service.phone_service import PhoneService
from src.service.process_manager_service import ProcessManagerService

import multiprocessing as mp
import threading as th
from queue import Queue
import requests as rq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def fetch_content(url: str, queue: any):
    print('Retrieving contents for page: ', url)
    content = rq.get(url, headers=headers).text
    print('Done retrieving contents for page: ', url)
    queue.put({
        'url': url,
        'content': content
    })


if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    url_map = {}
    website_infos = []
    queue = mp.Queue()
    content_queue = Queue()
    # singleton_data_context_manager = SingletonDataContextManager()
    # print(singleton_data_context_manager.get_queue())

    image_service = ImageService()
    phone_service = PhoneService()
    urls = [url for url in urls if url != '']
    functions_defs = [image_service.retrieve_logo_parallel, phone_service.retrieve_phones_parallel]
    # functions_defs = [phone_service.retrieve_phones_parallel]

    processes = []
    processes_limit = len(functions_defs)
    partition_size = int(len(urls) / processes_limit) + 1
    urls_partitioned = [urls[i * partition_size: (i + 1) * partition_size] for i in range(processes_limit)]
    if len(urls_partitioned[-1]) == 0:
        urls_partitioned = urls_partitioned[:-1]

    process_manager_service = ProcessManagerService()

    for partition in urls_partitioned:

        contents = []
        thread_pool = []
        for url in partition:
            function_args = (url, content_queue,)
            thread = th.Thread(target=fetch_content, args=function_args)
            thread_pool.append(thread)
            thread.start()

        for thread in thread_pool:
            thread.join()

        while not content_queue.empty():
            contents.append(content_queue.get())

        for function_def in functions_defs:
            args = (function_def, {'page_map': contents}, queue, len(partition),)
            process = mp.Process(target=process_manager_service.run_threads, args=args)
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        website_infos.append(queue.get())

    updated_attrs = []
    site_val = {}
    for info in website_infos:
        key = list(info.keys())[0]
        value = list(info.values())[0]

        if 'website' in value:
            site_val['website'] = value['website']
        if 'logo' in value:
            site_val['logo'] = value['logo']
        if 'phones' in value:
            site_val['phones'] = value['phones']

        if 'website' in site_val and 'logo' in site_val and 'phones' in site_val:
            updated_attrs.append(site_val)
            site_val = {}

    print(updated_attrs)

    # updated_attrs = []
    # data = {}
    # current_key = ''
    # for key, value in site_val.items():
    #     if current_key != key.split('_')[0]:
    #         if data:
    #             updated_attrs.append(data)
    #         current_key = key.split('_')[0]
    #
    #     key_name = key.split('_')[1]
    #     data[key_name] = value
    #
    #
    # print(updated_attrs)


    # for url in urls:
    #     if url == '':
    #         continue
    #
    #     print('Fetching >> ', url)
    #     try:
    #         response = rq.get(url, headers=headers)
    #         print('status_code >> ', response.status_code)
    #         if response.status_code in [400, 500, 403]:
    #             url_map.update({url: response.text})
    #             continue
    #
    #         logo_info = image_service.retrieve_logo(response.text)
    #         phones_info = phone_service.retrieve_phones(response.text)
    #         website_infos.append({
    #             'logo': image_service.normalize_path(url=url, image_url=logo_info.get('img')),
    #             'website': url,
    #             'phones': phones_info.get('phone_list')
    #         })
    #
    #     except Exception as e:
    #         print('error -> ', str(e))
    #     print()
    #
    # print('Unsuccessful URLs', url_map.keys())
    # print('Successful URLs', website_infos)

# https://www.illion.com.au
# https://www.phosagro.com/contacts
# https://www.powerlinx.com/contact
# https://www.cialdnb.com/en
# https://www.illion.com.au/contact-us
# https://en.cialdnb.com/
# https://www.cmsenergy.com/contact-us/default.aspx
# https://www.archdaily.com.br/br/905283/casa-do-boi-leo-romano-arquitetura
# https://www.vivareal.com.br/
# https://kemlu.go.id/portal/en
# https://www.kitano.com.br/receitas/frango-assado-com-salsa-e-cebolinha/
# https://www.tudogostoso.com.br/receita/80686-massa-de-coxinha-facil-da-andriele.html
