from src.utils.string_utils import *

def join_paths(url: str, image_url: str) -> str:
    if not is_non_null_nor_empty(image_url):
        return ''

    if image_url.startswith("http"):
        return image_url

    if image_url.startswith("//"):
        return 'https:' + image_url

    url_parts = url.split("/")

    return url_parts[0] + '//' + url_parts[2] + '/' + image_url
