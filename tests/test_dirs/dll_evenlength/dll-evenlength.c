/*
 * Doubly linked list of even length
 *
 * boxes:
 */

#include <stdlib.h>
typedef struct T1
{
    struct T1* next;
    struct T1* prev;
}* T;

int main()
{

    T x = NULL;
    T y = NULL;

    y = malloc(sizeof(*y));
    y->next = x;
    x = y;

    y = malloc(sizeof(*y));
    y->next = x;
    x->prev = y;
    x = y;

    while (*)
    {
        y = malloc(sizeof(*y));
        y->next = x;
        x->prev = y;
        x = y;

        y = malloc(sizeof(*y));
        y->next = x;
        x->prev = y;
        x = y;
    }

    while (y != NULL)
    {
        x = y;
        y = y->next;
        free(x);
        x = y;
        y = y->next;
        free(x);
    }

    return 0;
}
