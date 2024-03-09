from src.utils.string_utils import *

phone_accepted_tokens = {
    '(': True,
    ')': True,
    '+': True,
    '-': True
}


def phone_cleansing(phone: str) -> str:
    phone_cleansed = ''
    if is_non_null_nor_empty(phone):
        tokens = list(phone)
        for token in tokens:
            if token in phone_accepted_tokens:
                phone_cleansed += token
            else:
                if token.isdigit() or token == ' ':
                    phone_cleansed += token
                    continue

                phone_cleansed += ' '

    return phone_cleansed
