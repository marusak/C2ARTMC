#include <stdlib.h>

typedef struct linked_leaves_str {
    struct linked_leaves_str *left;
    struct linked_leaves_str *right;
    struct linked_leaves_str *parrent;
    struct linked_leaves_str *successor;
}* linked_leaves_str;

linked_leaves_str y,z,q;

/* We suppose, that the data structure is on the beginning pointed by variable x */

void main2(linked_leaves_str x) {
    y=x->left;
    while (y != NULL) {
        x = y;
        y = x->left;
    }
    q = x;
    y = q->parrent;
    while (y != NULL) {
        z = y->right;
        if (z == y) {
            q = y;
        } else {
            q = y->right;
            y = q->left;
            while (y != NULL) {
                q = y;
                y = q->left;
            }
            x->successor = q;
            x = q;
        }
        y = q->parrent;
    }
}
