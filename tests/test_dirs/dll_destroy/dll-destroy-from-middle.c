/*
 * Doubly linked list destroying from the middle
 *
 * boxes:
 */

#include <stdlib.h>

typedef struct node1 {
    struct node1 *l;
    struct node1 *r;
}* node;

int main()
{
    // create root
    node pt = malloc(sizeof(node));
    pt->l = NULL;
    pt->r = NULL;

    while (*) {
        node pn = pt;

        if (*) {
            // seek leftmost node
            while (pn)
                pn = pn->l;
        }
        else {
            // seek rightmost node
            while (pn)
                pn = pn->r;
        }

        // append a new node
        pn = malloc(sizeof(node));
        pn->l = NULL;
        pn->r = NULL;
    }

    // destroy left sublist
    while (pt->l) {
        node next = pt->l->l;
        free(pt->l);
        pt->l = next;
    }

    // destroy right sublist
    while (pt->r) {
        node next = pt->r->r;
        free(pt->r);
        pt->r = next;
    }

    // free root
    free(pt);
    return 0;
}
