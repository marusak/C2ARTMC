#include <stdlib.h>

typedef struct Dll {
    int data;
    struct Dll *next;
    struct Dll *prev;
} *dll;

dll element, tmp, tmp2;

/* t points to the head of the DLL */

void main2(dll t) {
    tmp = t;
    element = malloc(sizeof(struct Dll));
    if (element == NULL) return; /* ERROR, not alocated */
    element->data = 1;
    element->next = NULL;

    if (t == NULL) {
        element->prev = NULL;
        return;
    }

    tmp2 = tmp->next;
    while (tmp2 != NULL) {
        tmp = tmp->next;
        tmp2 = tmp->next;
    }
    tmp->next = element;
    element->prev = tmp;
    return;
}
