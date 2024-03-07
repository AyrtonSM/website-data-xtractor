from bs4 import BeautifulSoup
from src.utils.phone_utils import *
from src.enum.html_name import HtmlName
import re


class PhoneService:

    PHONE_KEY_MAP = 'phone_list'

    _bs_soup = None

    def retrieve_phones(self, content: str, parser: str = 'html.parser') -> dict:

        self._bs_soup = BeautifulSoup(content, parser)

        phone_url_map = {self.PHONE_KEY_MAP: []}

        spans = self._bs_soup.find_all(HtmlName.Span.value)
        for span in spans:
            self._find_phones_by_regex(span.text, phone_url_map)

        anchors = self._bs_soup.find_all(HtmlName.Anchor.value)
        for anchor in anchors:
            if anchor.has_attr(HtmlName.Href.value):
                if 'tel:' in anchor[HtmlName.Href.value]:
                    self._find_phones_by_regex(anchor.text, phone_url_map)

        paragraphs = self._bs_soup.find_all(HtmlName.Paragraph.value)
        for paragraph in paragraphs:
            paragraph = paragraph.text.replace('\n', ' ').strip()
            self._find_phones_by_regex(paragraph, phone_url_map)

        cleansed_phones = list(set([phone_cleansing(phone) for phone in phone_url_map.get('phone_list')]))
        phone_url_map.update({
            self.PHONE_KEY_MAP: cleansed_phones
        })

        return phone_url_map

    @staticmethod
    def _find_phones_by_regex(content: str, phone_url_map: dict):
        numbers = re.findall(r'(?:\(?\+?\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{1,7}[\s.-]?\d{1,7}', content)
        if len(numbers) > 0:
            for num in numbers:
                if len(num) >= 8:
                    phone_url_map.get(PhoneService.PHONE_KEY_MAP).append(num.strip())
