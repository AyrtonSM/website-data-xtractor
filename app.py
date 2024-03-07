import sys
import requests as rq
from src.service.image_service import ImageService
from src.service.phone_service import PhoneService

if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    url_map = {}
    website_infos = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    image_service = ImageService()
    phone_service = PhoneService()

    if urls[-1] == '':
        urls = urls[:len(urls) - 1]

    for url in urls:
        print('Fetching >> ', url)
        try:
            response = rq.get(url, headers=headers)
            print('status_code >> ', response.status_code)
            if response.status_code in [400, 500, 403]:
                url_map.update({url: response.text})
                continue

            logo_info = image_service.retrieve_logo(response.text)
            phones_info = phone_service.retrieve_phones(response.text)
            website_infos.append({
                'logo': image_service.normalize_path(url=url, image_url=logo_info.get('img')),
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
# https://kemlu.go.id/portal/en
