#include <stdlib.h>
#include <verifier-builtins.h>

typedef struct T1 {
    struct T1* next;
    struct T1* prev;
    int data;
}* T;

int main() {
    T x = NULL;
    T y = NULL;

    while (*) {
        y = malloc(sizeof(T));
        y->next = x;
        y->prev = NULL;
        y->data = 0;
        if (x)
            x->prev = y;
        x = y;
    }

    y = x;

    while (y != NULL) {
        if (*) {
        T z = malloc(sizeof(T));
        z->next = y->next;
        z->prev = y;
        y->next = z;
        if (z->next)
            z->next->prev = z;
        break;
    }
    y = y->next;
    }

    while (x != NULL) {
    y = x;
        x = x->next;
    free(y);
    }

    return 0;
}
