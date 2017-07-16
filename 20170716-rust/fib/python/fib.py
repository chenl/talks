#!/usr/bin/env python3

def fib(n: int) -> int:
    if n < 3:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

if __name__ == '__main__':
    print("{}".format(fib(40)))
