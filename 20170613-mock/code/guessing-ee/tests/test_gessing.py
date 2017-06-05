# -*- coding: utf-8 -*-

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from unittest import mock
except ImportError:
    import mock

from guessing import game


# TODO: use @mock.patch.multiple() here
# https://docs.python.org/3/library/unittest.mock.html#patch-multiple
@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('random.seed')
@mock.patch('sys.stdout' , new_callable=StringIO)
def test_intro(mock_stdout, mock_seed, mock_T):
    game.intro()
    msg = "I am bored, lets play a game."
    mock_T.assert_called_once_with(msg)
    mock_seed.assert_called_once_with()
    assert mock_stdout.getvalue() == "{}\n".format(msg)

@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('sys.stdout' , new_callable=StringIO)
def test_outro(mock_stdout, mock_T):
    game.outro()
    msg = "That was fun! Thank you for playing with me."
    mock_T.assert_called_once_with(msg)
    assert mock_stdout.getvalue() == "{}\n".format(msg)
