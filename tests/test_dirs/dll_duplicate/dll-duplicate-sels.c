/*
 * Doubly linked list construction and deletion.
 */

#include <stdlib.h>
#include <verifier-builtins.h>
typedef struct T1 {
    struct T1* next1;
    struct T1* next2;
    struct T1* prev1;
    struct T1* prev2;
    int data;
}* T;

int main() {


    T x = NULL;
    T y = NULL;

    x = malloc(sizeof(T));
    x->next1 = NULL;
    x->next2 = NULL;
    x->prev1 = NULL;
    x->prev2 = NULL;

    while (*) {
        y = malloc(sizeof(T));
        y->next1 = x;
        y->next2 = x;
        x->prev1 = y;
        x->prev2 = y;
        y->prev1 = NULL;
        y->prev2 = NULL;
        x = y;
    }

    while (x) {
        y = x->next1;
        free(x);
        x = y;
    }

    return 0;
}
