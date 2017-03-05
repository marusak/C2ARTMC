/*
 * Doubly linked list construction and deletion. The construction is done in two
 * ways (forward and backward).
 */

#include <stdlib.h>
typedef struct T1 {
    struct T1* next;
    struct T1* prev;
    int data;
}* T;

int main() {

    T x = NULL;
    T y = NULL;

    x = malloc(sizeof(T));
    x->next = NULL;
    x->prev = NULL;

    // first DLL
    while (*) {
        y = malloc(sizeof(T));
        y->next = x;
        x->prev = y;
        y->prev = NULL;
        x = y;
    }

    T z = NULL;

    y = malloc(sizeof(T));
    y->next = NULL;
    y->prev = NULL;

    // pointer to the end of y
    T yLast = y;

    // second DLL
    while (*) {
        z = malloc(sizeof(T));
        z->next = y;
        y->prev = z;
        z->prev = NULL;
        y = z;
    }

    // concat 'x' and 'y'
    yLast->next = x;
    x->prev = yLast;

    y = NULL;
    z = NULL;

    y = x;
    while (y) {
        y = y->next;
    }

    // delete
    while (x->next) {
        y = x->next;
        x->next = x->next->next;
        free(y);
    }

    while (x->prev) {
        y = x->prev;
        x->prev = x->prev->prev;
        free(y);
    }

    free(x);

    return 0;
}

