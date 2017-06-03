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

@mock.patch('guessing.game.T', side_effect=lambda x: x)
@mock.patch('sys.stdout' , new_callable=StringIO)
def test_outro(mock_stdout, mock_T):
    game.outro()
    assert mock_stdout.getvalue() == "That was fun! Thank you for playing with me.\n"
