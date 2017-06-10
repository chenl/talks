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

@mock.patch('guessing.i18n.lang', return_value='C')
@mock.patch('sys.stdin.readline', return_value='15\n')
@mock.patch('sys.stdout', new_callable=StringIO)
def test_your_guess_num(mock_stdout, mock_readline, mock_lang):
    assert game.your_guess() == 15
    assert mock_stdout.getvalue() == "Your guess is:\n"

@mock.patch('guessing.i18n.lang', return_value='C')
@mock.patch('sys.stdin.readline', side_effect=[
    'hello\n', '42\n'])
@mock.patch('sys.stdout', new_callable=StringIO)
def test_your_guess_2nd_try(mock_stdout, mock_readline, mock_lang):
    assert game.your_guess() == 42
    assert mock_stdout.getvalue() == (
        "Your guess is:\n"
        "Sorry, I didn't get that\n"
        "Your guess is:\n"
    )

@mock.patch('guessing.i18n.lang', return_value='C')
@mock.patch('sys.stdin.readline', side_effect=['stop\n'])
@mock.patch('sys.stdout', new_callable=StringIO)
def test_your_guess_quit(mock_stdout, mock_readline, mock_lang):
    assert game.your_guess() is None
    assert mock_stdout.getvalue() == (
        "Your guess is:\n"
    )


def test_PromptGGEE():
    prompt = game.PromptGGEE(level=3, max_num=7, num=5)
    assert '{0:0} {0:1} {0:2}'.format(prompt) == '3 7 5'
    assert '{a} {b:1} {c}'.format(a='a', b=prompt, c='c') == 'a 7 c'
    assert 'simple'.format(prompt) == 'simple'


@pytest.mark.parametrize('guesses,expected_messages', [
    ([4, 6, 5], [  # full scenario
        "Level {0:0}: 0 to {0:1}",
        "Can you guess what number I am thinking about?",
        "No, my number is bigger than that",
        "Can you guess what number I am thinking about?",
        "No, my number is smaller than that",
        "Can you guess what number I am thinking about?",
        "Yes, this is the number I was thinking about! How did you know that?",
    ]),
    ([None], [     # empty scenario
        "Level {0:0}: 0 to {0:1}",
        "Can you guess what number I am thinking about?",
        "Just wanted you to know that I was thinking about {0:2}",
    ]),
    ([5], [        # lucky scenario
        "Level {0:0}: 0 to {0:1}",
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

    assert mock_T.call_args_list == map(mock.call, expected_messages)

    prompt = game.PromptGGEE(level=level, max_num=7, num=num)
    printed_messages = [msg.format(prompt) + '\n'
                        for msg in expected_messages]
    assert mock_stdout.getvalue() == ''.join(printed_messages)
