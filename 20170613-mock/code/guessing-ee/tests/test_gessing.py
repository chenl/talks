# -*- coding: utf-8 -*-

import pytest

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from unittest import mock
except ImportError:
    import mock

with mock.patch('google.cloud.translate.Client'):
    from guessing import game


@pytest.mark.parametrize('fun_times', [0, 1, 5])
def test_game(fun_times):
    # given
    with mock.patch.multiple('guessing.game',
                             intro=mock.DEFAULT,
                             play=mock.DEFAULT,
                             was_this_fun=mock.DEFAULT,
                             outro=mock.DEFAULT):
        game.was_this_fun.side_effect = [True] * fun_times + [False]
        # when
        game.game()
        # then
        game.intro.assert_called_once()
        assert game.play.call_count == 1 + fun_times
        game.outro.assert_called_once()

@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('random.seed')
@mock.patch('sys.stdout' , new_callable=StringIO)
def test_intro(mock_stdout, mock_seed, mock_T):
    game.intro()
    msg = "I am bored, let's play a game."
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

def test_max_number():
    assert game.max_number(1) == 1
    assert game.max_number(2) == 3
    assert game.max_number(3) == 7
