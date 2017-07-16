#include <stdio.h>

int fib(int n) {
    if (n < 3) {
        return 1;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
}

int main() {
    printf("%d\n", fib(40));
    return 0;
}
