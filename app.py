import sys
from bs4 import BeautifulSoup
import json
import requests as rq

if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    if urls[-1] == '':
        urls = urls[:len(urls)-1]

    for url in urls:
        response = rq.get(url)
        print('-->',response.status_code)

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            print()
            print(url)
            print(soup.findAll('svg'))
            print(soup.findAll('img'))
            print()


