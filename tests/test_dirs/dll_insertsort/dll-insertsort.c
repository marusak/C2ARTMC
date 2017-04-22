/*
 * Doubly linked list insert-sort
 *
 * boxes: genericdll.boxes
 */

#include <stdlib.h>
#include <verifier-builtins.h>
typedef struct T1 {
    struct T1* next;
    struct T1* prev;
}* T;

int main() {


    T x = NULL;
    T y = NULL;

    while (*) {
        y = malloc(sizeof(T));
        y->next = x;
        y->prev = NULL;
        if (x)
            x->prev = y;
        x = y;
    }

    T sorted = NULL;
    T pred = NULL;
    T z = NULL;

    while (x) {
        y = x;
        x = x->next;
        z = sorted;
        pred = NULL;

        while (z && *) {
            pred = z;
            z = z->next;
        }

        y->next = z;
        if (z) z->prev = y;
        y->prev = pred;
        if (pred) pred->next = y;
        else sorted = y;
    }

    while (sorted != NULL) {
        y = sorted;
        sorted = sorted->next;
        free(y);
    }

    return 0;
}
