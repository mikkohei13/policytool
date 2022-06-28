import string
from itertools import permutations

import pycountry


def available_language_codes() -> dict[str, str]:
    """
    Returns a dict of available language codes in the form:
        the language 2-letter alpha code -> language name
    """
    languages = {}
    for letter_1, letter_2 in permutations(string.ascii_lowercase, 2):
        code = f'{letter_1}{letter_2}'
        lang = pycountry.languages.get(alpha_2=code)
        if lang and code:
            languages[code] = lang.name
    return languages
