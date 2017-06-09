# -*- coding: utf-8 -*-

import pytest

try:
    from io import StringIO
except ImportError:
    #from io import BytesIO as StringIO
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


@mock.patch('random.seed')
@mock.patch('guessing.game.print')
@mock.patch('guessing.game.T', side_effect=lambda x: x)
def test_intro(mock_T, mock_print, mock_seed):
    game.intro()
    msg = "I am bored, let's play a game."
    mock_T.assert_called_once_with(msg)
    mock_print.asseret_called_once_with(msg)
    mock_seed.assert_called_once_with()


@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('sys.stdout', new_callable=StringIO)
def test_outro(mock_stdout, mock_T):
    game.outro()
    msg = "That was fun! Thank you for playing with me."
    mock_T.assert_called_once_with(msg)
    assert mock_stdout.getvalue() == "{}\n".format(msg)


def test_max_number():
    assert game.max_number(1) == 1
    assert game.max_number(2) == 3
    assert game.max_number(3) == 7


@pytest.mark.parametrize('guesses,expected_messages', [
    ([4, 6, 5], [  # full scenario
        "Level 3: 0 to 7",
        "Can you guess what number I am thinking about?",
        "No, my number is bigger than that",
        "Can you guess what number I am thinking about?",
        "No, my number is smaller than that",
        "Can you guess what number I am thinking about?",
        "Yes, this is the number I was thinking about! How did you know that?",
    ]),
    ([None], [     # empty scenario
        "Level 3: 0 to 7",
        "Can you guess what number I am thinking about?",
        "Just wanted you to know that I was thinking about 5",
    ]),
    ([5], [        # lucky scenario
        "Level 3: 0 to 7",
        "Can you guess what number I am thinking about?",
        "Yes, this is the number I was thinking about! How did you know that?",
    ]),
])
@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('sys.stdout', new_callable=StringIO)
def test_play(mock_stdout, mock_T, guesses, expected_messages):
    level = 3
    num = 5

    with \
            mock.patch('guessing.game.think_of_a_number', return_value=num), \
            mock.patch('guessing.game.your_guess', side_effect=guesses):
        game.play(level)

    mock_T.call_args_list = map(mock.call, expected_messages)
    assert mock_stdout.getvalue() == '\n'.join(expected_messages) + '\n'
