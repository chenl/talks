#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Guessing Game - the Enterprise Edition
"""

from __future__ import print_function
import sys
import random
import itertools

from .i18n import T, is_yes, is_quit

__authors__ = ["Chen Rotem Levy", "Eliad Levy"]  # no relation
__version__ = "0.1.0"
__license__ = "Apache 2.0"


# TODO: implement a high-score
# see https://github.com/chenl/talks/issues/4

class PromptGGEE(object):
    """This class was made to work around a problem,
     where a string is translated before formatting.

     E.g. a part like `{level}` might translate too,
     thus breaking the formatting.

     This class allows to replace `{level}` with `{0:0}`:
     >>> prompt = PromptGGEE(3, 7, 5)
     >>> 'using level {0:0}'.format(prompt)

     Using a fixed mapping between indices (0) and attrs (level),
     we prevent the translation of any attr.
    """

    attr_by_index = {'0': 'level', '1': 'max_num', '2': 'num'}

    def __init__(self, level, max_num, num):
        self.level = str(level)
        self.max_num = str(max_num)
        self.num = str(num)

    def __getitem__(self, item):
        attr = self.attr_by_index[item]
        return getattr(self, attr)

    def __format__(self, format_spec):
        return self[format_spec]

def game():
    # type: () -> None
    intro()
    for level in itertools.count(1):
        play(level)
        if not was_this_fun():
            break
    outro()

def intro():
    # type: () -> None
    print(T("I am bored, let's play a game."))
    random.seed()

def outro():
    # type: () -> None
    print(T("That was fun! Thank you for playing with me."))

def max_number(level):
    # type: (int) -> int
    return (1 << level) - 1

def think_of_a_number(level):
    # type: () -> int
    return random.randint(0, max_number(level))

def play(level):
    # type: (int) -> None
    print(T("Level {level}: 0 to {max_num}").format(
        level=level, max_num=max_number(level)))
    num = think_of_a_number(level)
    while True:
        print(T("Can you guess what number I am thinking about?"))
        guess = your_guess()
        if guess is None:
            print(T("Just wanted you to know that I was thinking about {}").format(num))
            break
        if guess < num:
            print(T("No, my number is bigger than that"))
        elif guess > num:
            print(T("No, my number is smaller than that"))
        else:
            print(T("Yes, this is the number I was thinking about! How did you know that?"))
            break

def your_guess():
    # type: () -> Optional[int]
    while True:
        print(T("Your guess is:"))
        answer = sys.stdin.readline()
        if is_quit(answer):
            return None
        try:
            return int(answer)
        except ValueError:
            print(T("Sorry, I didn't get that"))

def was_this_fun():
    # type: () -> bool
    print(T("I enjoyed that. Shall we play again?"))
    return is_yes(sys.stdin.readline())

if __name__ == '__main__':
    game()
