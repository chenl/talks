# -*- coding: utf-8 -*-

from os import environ
from itertools import chain
from google.cloud import translate

CLIENT = translate.Client()

def lang():
    # type: () -> str
    lang_keys = ('LC_MESSAGES', 'LANG', 'LC_ALL')
    lang_env = (environ.get(key) for key in lang_keys)
    return next(filter(None, chain(lang_env, 'C')))[:2]

def is_quit(text):
    # type: (str) -> bool
    if lang() == 'he':
        return text.strip() in ['לא', 'די', 'מספיק', 'צא בחוץ']
    else:
        return text.strip().lower() in ['quit', 'stop', 'exit', 'no', 'enough']

def is_yes(text):
    # type: (str) -> bool
    if lang == 'he':
        return text.strip() in ['כ', 'כן', 'בטח', 'סבבה', '']
    else:
        return text.strip().lower() in ['', 'y', 'yes', 'yep', 'sure']

def T(text):
    # type: (str) -> str
    lng = lang()
    if lng in ('C', 'en'):
        return text
    tr = CLIENT.translate(
        values=text,
        format_='text',
        target_language=lng,
        source_language='en')
    return tr[0]['translatedText']
