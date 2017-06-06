# -*- coding: utf-8 -*-

try:
    from unittest import mock
except ImportError:
    import mock

from guessing import i18n


@mock.patch.dict('guessing.i18n.environ', LC_MESSAGES='he_IL')
def test_lang_lc_message_he():
    assert i18n.lang() == 'he'

def test_lang_default():
    with mock.patch.dict('guessing.i18n.environ', clear=True):
        assert i18n.lang() == 'C'

def test_is_lang_en():
    with mock.patch.dict('guessing.i18n.environ',
                         dict(LC_ALL='en_US',
                              LC_MESSAGES='en_US',
                              LANG='en_US')):
        assert i18n.lang() == 'en'

@mock.patch('guessing.i18n.lang')
def test_T_not_hebrew(mock_lang):
    mock_lang.return_value = 'C'
    assert i18n.T('hello') == 'hello'

@mock.patch('guessing.i18n.CLIENT')
@mock.patch('guessing.i18n.lang')
def test_T_hebrew(mock_is_lang, mock_CLIENT):
    mock_lang.side_effect = lambda lang: lang == 'he'
    assert i18n.T('hello') == 'OLLEH'


def test_is_quit_english():
    with mock.patch('guessing.i18n.is_lang', return_value=False):
        assert i18n.is_quit('QUIT')
        assert i18n.is_quit('stop')
        assert i18n.is_quit('exit')
        assert not i18n.is_quit('')
        assert not i18n.is_quit('I want my Mummy!')
        assert not i18n.is_quit('q')
        assert not i18n.is_quit('די')

def test_is_quit_hebrew():
    with mock.patch('guessing.i18n.is_lang', return_value=True):
        assert i18n.is_quit('די')
        assert i18n.is_quit('מספיק')
        assert i18n.is_quit('צא בחוץ')
        assert not i18n.is_quit('')
        assert not i18n.is_quit('אני רוצה לאימא')
        assert not i18n.is_quit('quit')


@mock.patch('guessing.i18n.is_lang', return_value=False)
def test_is_yes_english(_):
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
    assert i18n.is_yes('  בטח')
    assert i18n.is_yes('סבבה')
    assert not i18n.is_yes('yes')
