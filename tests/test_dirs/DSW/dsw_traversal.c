#include <stdlib.h>

typedef struct tree1 {
    int data;
    struct tree1 *left;
    struct tree1 *right;
}* tree;

/* We suppose, that the data structure is on the beginning pointed by variable x */

void dsw(tree x) {
    tree y, t;
    t = NULL;
    if (x == NULL)
        return;
    while (any) {
        if (x->data == 2) {
            y = x;
            x = t;
            if (x == NULL) return;
            if (x->data == 0) {
                t = x->right;
                x->right = y;
                x->data = 1;
            } else {
                t = x->left;
                x->left = y;
                x->data = 2;
            }
        } else {
            if (x->data == 1) {
                y = x->left;
                if (y == NULL)
                    x->data = 2;
                else {
                    x->left = t;
                    t = x;
                    x = y;
                }
            } else {
                y = x->right;
                if (y == NULL)
                    x->data = 1;
                else {
                    x->right = t;
                    t = x;
                    x = y;
                }
            }
        }
    }
}
