#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from unittest import mock
import builtins
import pytest


# Code:

def get_json(filename):
    try:
        return json.loads(open(filename).read())
    except (IOError, ValueError):
        return {}

# Tests:

@mock.patch('builtins.open')
def test_json(mock_open):
    # given
    mock_open.return_value.read.return_value = '{"spam": 42}'

    # when
    actual = get_json('some_file.json')

    # then
    mock_open.assert_called_once_with('some_file.json')
    expected = {'spam': 42}
    assert actual == expected

@mock.patch('builtins.open')
def test_json_io_error(mock_open):
    mock_open.side_effect = IOError
    get_json('non_exists') == {}

@moch.patch('json.loads')
@mock.patch('builtins.open')
def test_json_value_error(mock_open, mock_loads):
    mock_loads.side_effect = ValueError('Doh!')
    get_json('non_exists') == {}

if __name__ == '__main__':
    test_json()
