# -*- coding: utf-8 -*-

from os import environ

def is_lang(lang):
    return any(environ.get(key, 'C').startswith(lang)
               for key in ('LC_MESSAGES', 'LC_ALL', 'LANG'))

def T(text):
    if is_lang('he'):
        return text[::-1].upper()
    else:
        return text

def is_quit(text):
    # type: (str) -> bool
    if is_lang('he'):
        return test.strip() in ['לא', 'די', 'מספיק', 'חלאס']
    else:
        return text.strip().lower() in ['quit', 'stop', 'no', 'enough']

def is_yes(text):
    # type: (str) -> bool
    if is_lang('he'):
        return test.strip() in ['כ', 'כן', 'בטח', 'סבבה']
    else:
        return text.strip().lower() in ['y', 'yes', 'yep', 'sure']