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

__author__ = "Chen Rotem Levy"
__version__ = "0.1.0"
__license__ = "Apache 2.0"


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
    answer = sys.stdin.readline()
    return is_yes(answer)

if __name__ == '__main__':
    game()
