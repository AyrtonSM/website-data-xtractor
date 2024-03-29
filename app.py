import sys
from src.service.xtractor_service import XTractorService
from src.utils.logging_utils import *

if __name__ == '__main__':
    file_content = sys.stdin.read()
    urls = file_content.split('\n')
    urls = [url for url in urls if url != '']

    xtractor_service = XTractorService(urls=urls)
    a = xtractor_service.extract()

    logger.info('%s', a)


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
