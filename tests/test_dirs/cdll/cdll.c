/*
 * Circular doubly linked list insertion and deletion.
 */

#include <stdlib.h>
#include <verifier-builtins.h>

typedef struct T1 {
    struct T1* next;
    struct T1* prev;
    int data;
}* T;

T tmp;

int main() {
    T x = NULL;
    T y = NULL;

    x = malloc(sizeof(struct T));
    x->next = x;
    x->prev = x;
    x->data = 0;

    while (*) {
        y = malloc(sizeof(struct T));
        y->next = x->next;
        tmp = y->next
        tmp->prev = y;
        y->prev = x;
        y->data = 0;
        x->next = y;
        y = NULL;
    }

    y = x->next;

    while (y != x) {
        T z = y;
        y = y->next;
        free(z);
    }

    free(x);

    return 0;

}
