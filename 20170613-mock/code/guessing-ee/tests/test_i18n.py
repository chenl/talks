# -*- coding: utf-8 -*-

try:
    from unittest import mock
except ImportError:
    import mock

from guessing import i18n


def test_is_lang_default():
    with mock.patch.dict('guessing.i18n.environ', clear=True):
        assert i18n.is_lang('C')

def test_is_lang_default_not_english():
    with mock.patch.dict('guessing.i18n.environ', clear=True):
        assert not i18n.is_lang('en')

def test_is_lang_not_hebrew():
    with mock.patch.dict('guessing.i18n.environ',
                         dict(LC_ALL='en_US',
                              LC_MESSAGES='en_US',
                              LANG='en_US')):
        assert not i18n.is_lang('he')

def test_is_lang_hebrew():
    with mock.patch.dict('guessing.i18n.environ',
                         LC_MESSAGES='he_IL'):
        assert i18n.is_lang('he')


@mock.patch('guessing.i18n.is_lang')
def test_T_not_hebrew(mock_is_lang):
    mock_is_lang.return_value = False
    assert i18n.T('hello') == 'hello'

@mock.patch('guessing.i18n.is_lang')
def test_T_hebrew(mock_is_lang):
    mock_is_lang.side_effect = lambda lang: lang == 'he'
    assert i18n.T('hello') == 'OLLEH'


@mock.patch('guessing.i18n.is_lang', return_value=False)
def test_is_yes_english(mock_is_lang):
    mock_is_lang.return_value = False
    assert i18n.is_yes('')
    assert i18n.is_yes('   yes')
    assert i18n.is_yes('y')
    assert i18n.is_yes('YEP  ')
    assert i18n.is_yes('  sure  ')
    assert not i18n.is_yes('no')
    assert not i18n.is_yes('maybe')
    assert not i18n.is_yes('you tell me')
    assert not i18n.is_yes('כן')


@mock.patch('guessing.i18n.is_lang', return_value=True)
def test_is_yes_hebrew(_):
    assert i18n.is_yes('')
    assert i18n.is_yes('כן')
    assert i18n.is_yes('כ')
    assert i18n.is_yes('בטח')
    assert i18n.is_yes('סבבה')
    assert not i18n.is_yes('yes')
