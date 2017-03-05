/*
 * A doubly linked list that is manipulated in such a way that only keeps the
 * SLL shape ok (i.e. prev links are broken)
 */

#include <stdlib.h>
#include <verifier-builtins.h>

typedef struct T1
{
    struct T1* next;
    struct T1* prev;
}* T;

T tmp;

int main()
{

    T x = NULL;
    T y = NULL;
    T z = NULL;

    x = malloc(sizeof(T));
    x->next = NULL;
    x->prev = NULL;

    // create the DLL
    while (*)
    {
        y = malloc(sizeof(T));
        y->next = x;
        x->prev = y;
        y->prev = NULL;
        x = y;
    }

    // 'x' is now the head

    // now we randomly erase a few elements, keeping only the 'next' pointers
    // consistent
    while (*)
    {
        y = x;

        while (y->next && *)
        {
            y = y->next;
        }

        if (y->next)
        {
            tmp = y->next;
            z = tmp->next;
            free(y->next);
            y->next = z;
        }
    }

    while (x->next)
    {
        y = x->next;
        tmp = x->next;
        x->next = tmp->next;
        free(y);
    }

    free(x);

    return 0;
}
