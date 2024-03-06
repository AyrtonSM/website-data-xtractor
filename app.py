import sys
from bs4 import BeautifulSoup
import json
import requests as rq
import re

suggested_attrs_by_html_tag = {
    'div' : ['logo', 'navbar_logo'],
    'img' : ['logo', 'img_logo', 'light-logo']
}


def retrieve_logo(soup: BeautifulSoup) -> dict:
    logo_url_map = {'img' : ''}

    keyword = 'logo'
    anchors = soup.find_all('a')

    for anchor in anchors:
        imgs = anchor.find_all('img')

        if len(imgs) == 0:
            continue

        for img in imgs:
            print(img)
            if img.has_attr('class'):
                for class_name in img['class']:
                    if keyword in class_name:
                        logo_url_map.update({'img': img['src']})
                        print('ok 1')
                        return logo_url_map

            if img.has_attr('alt'):
                if keyword in img['alt']:
                    logo_url_map.update({'img': img['src']})
                    print('ok 3')
                    return logo_url_map

            if img.has_attr('src'):
                normalized_src = img['src'].lower()
                if keyword in normalized_src:
                    logo_url_map.update({'img': img['src']})
                    print('ok 2')
                    return logo_url_map

    return logo_url_map


def retrieve_phones(soup: BeautifulSoup):
    phone_url_map = {'phone_list' : []}

    spans = soup.find_all('span')
    for span in spans:
        numbers = re.findall(r'(?:\+?\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{1,5}[\s.-]?\d{1,5}', span.text)
        if len(numbers) > 0:
            for num in numbers:
                if len(num) >= 8:
                    phone_url_map.get('phone_list').append(num.strip())

    anchors = soup.find_all('a')
    for anchor in anchors:
        if anchor.has_attr('href'):
            if 'tel:' in anchor['href']:
                numbers = re.findall(r'(?:\+?\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{1,5}[\s.-]?\d{1,5}', anchor.text)
                if len(numbers) > 0:
                    for num in numbers:
                        if len(num) >= 8:
                            phone_url_map.get('phone_list').append(num.strip())

    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        paragraph = paragraph.text.replace('\n', ' ').strip()
        numbers = re.findall(r'(?:\+?\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{1,5}[\s.-]?\d{1,5}', paragraph)
        if len(numbers) > 0:
            for num in numbers:
                if len(num) >= 8:
                    phone_url_map.get('phone_list').append(num.strip())

    phone_url_map = {'phone_list': list(set(phone_url_map.get('phone_list')))}
    return phone_url_map


if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    url_map = {}
    website_infos = []
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
            logo_info = retrieve_logo(soup=soup)
            phones_info = retrieve_phones(soup=soup)

            website_infos.append({
                'logo': logo_info.get('img'),
                'website': url,
                'phones': phones_info.get('phone_list')
            })


        except Exception as e:
            print('error -> ', str(e))
        print()

    print('Unsuccessful URLs', url_map.keys())
    print('Successful URLs', website_infos)



# https://www.illion.com.au
# https://www.phosagro.com/contacts
# https://www.powerlinx.com/contact
# https://www.cialdnb.com/en
# https://www.illion.com.au/contact-us
# https://en.cialdnb.com/
# https://www.cmsenergy.com/contact-us/default.aspx
# https://www.archdaily.com.br/br/905283/casa-do-boi-leo-romano-arquitetura
# https://www.vivareal.com.br/
