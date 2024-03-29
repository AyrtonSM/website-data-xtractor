from bs4 import BeautifulSoup
from src.utils.image_utils import *
from src.enum.html_name import HtmlName
from src.utils.logging_utils import *


class ImageService:
    _bs_soup = None

    def retrieve_logo_parallel(self, content: str, url: str, queue: any, parser: str = 'html.parser'):
        try:
            self._bs_soup = BeautifulSoup(content, parser)

            logo_url_map = {HtmlName.Image.value: ''}

            keyword = 'logo'

            images = self._bs_soup.find_all(HtmlName.Image.value)

            if len(images) > 0:
                self._image_retrieval(images, keyword, logo_url_map)

            logo_url_map.update({
                HtmlName.Image.value: self.normalize_path(url=url, image_url=logo_url_map.get(HtmlName.Image.value))
            })

            queue.put({
                url: {
                    'logo': logo_url_map.get(HtmlName.Image.value),
                    'website': url
                }
            })

        except Exception as e:
            logger.error(e)

    def _image_retrieval(self, images, keyword, logo_url_map):

        for img in images:
            self.build_logo_mapping(keyword=keyword, img=img, attribute=HtmlName.Class.value,
                                                               logo_url_map=logo_url_map)
            if is_non_null_nor_empty(logo_url_map.get(HtmlName.Image.value)):
                break

            self.build_logo_mapping(keyword=keyword, img=img, attribute=HtmlName.Alt.value,
                                                               logo_url_map=logo_url_map)
            if is_non_null_nor_empty(logo_url_map.get(HtmlName.Image.value)):
                break

            self.build_logo_mapping(keyword=keyword, img=img, attribute=HtmlName.Src.value,
                                                               logo_url_map=logo_url_map)
            if is_non_null_nor_empty(logo_url_map.get(HtmlName.Image.value)):
                break

    @staticmethod
    def update_logo_url_map(keyword: str, property_content: str, image_src_content: str,
                            logo_url_map: dict) -> (bool, dict):
        if keyword in property_content:
            logo_url_map.update({HtmlName.Image.value: image_src_content})
            return True, logo_url_map

        return False, logo_url_map

    def build_logo_mapping(self, keyword: str, img: any, attribute: str, logo_url_map: dict) -> (bool, dict):
        if img.has_attr(attribute):
            property_content = ''
            if attribute == HtmlName.Src.value:
                property_content = img[HtmlName.Src.value].lower()
            elif attribute == HtmlName.Alt.value:
                property_content = img[HtmlName.Alt.value]
            elif attribute == HtmlName.Class.value:
                for class_name in img[HtmlName.Class.value]:
                    is_present, logo_url_map = self.update_logo_url_map(
                        keyword=keyword,
                        property_content=class_name,
                        image_src_content=img[HtmlName.Src.value],
                        logo_url_map=logo_url_map
                    )

                    if is_present:
                        return is_present, logo_url_map

            is_present, logo_url_map = self.update_logo_url_map(
                keyword=keyword,
                property_content=property_content,
                image_src_content=img[HtmlName.Src.value],
                logo_url_map=logo_url_map
            )

            if is_present:
                return is_present, logo_url_map

    @staticmethod
    def normalize_path(url: str, image_url: str):
        return join_paths(url=url, image_url=image_url)
