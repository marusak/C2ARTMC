/*
 * Doubly linked list construction and deletion.
 */

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

    x = malloc(sizeof(T));
    x->next = NULL;
    x->prev = NULL;

    while (*) {
        y = malloc(sizeof(T));
        y->next = x;
        x->prev = y;
        y->prev = NULL;
        x = y;
    }

    while (x != NULL) {
        y = x->next;
        free(x);
        x = y;
    }

    return 0;
}
