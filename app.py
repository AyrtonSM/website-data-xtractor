import sys
from bs4 import BeautifulSoup
import json
import requests as rq

suggested_attrs_by_html_tag = {
    'div' : ['logo', 'navbar_logo'],
    'img' : ['logo', 'img_logo', 'light-logo']
}

logo_url_map = {}
def retrieve_logo(soup: BeautifulSoup) -> str:

    # html_tags = suggested_attrs_by_html_tag.keys()
    # for tag in html_tags:
    #     all_known_tags = [soup.find_all(tag, {"class": attr}) for attr in suggested_attrs_by_html_tag[tag]]
    #     print(all_known_tags)
    # print('aaaa')
    keyword = 'logo'

    anchors = soup.find_all('a')
    main_class_attr_name = None



    for anchor in anchors:
        imgs = anchor.find_all('img')
        if len(imgs) == 0:
            continue

        for img in imgs:

            normalized_src = img['src'].lower()

            if keyword in normalized_src:

                logo_url_map.update({'img': img['src']})
                main_class_attr_name = ''
                break

            if img.alt != '':
                if keyword in img.alt:
                    main_class_attr_name = img.alt
                    break

            for class_name in img['class']:
                if keyword in class_name:
                    main_class_attr_name = class_name
                    break

            if main_class_attr_name is not None:
                break

        if main_class_attr_name is not None:
            break

    print('class_name :', main_class_attr_name)
    print('logo_url :', logo_url_map)
def retrieve_phones(soup: BeautifulSoup):

    pass


if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    url_map = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    if urls[-1] == '':
        urls = urls[:len(urls)-1]

    for url in urls:
        print('Fetching >> ', url)
        try:
            response = rq.get(url, headers=headers)
            print('status_code >> ', response.status_code)
            if response.status_code in [400, 500, 403]:
                url_map.update({url: response.text})
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            retrieve_logo(soup=soup)


        except Exception as e:
            print('error -> ', str(e))
        print()

    print('Unsuccessful URLs', url_map.keys())



# https://www.illion.com.au
# https://www.phosagro.com/contacts
# https://www.powerlinx.com/contact
# https://www.cialdnb.com/en
# https://www.illion.com.au/contact-us
# https://en.cialdnb.com/
# https://www.cmsenergy.com/contact-us/default.aspx

