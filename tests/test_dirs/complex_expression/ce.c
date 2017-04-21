#include <stdlib.h>

typedef struct tree1 {
    int data;
    struct tree1 *left;
    struct tree1 *right;
    struct tree1 *parrent;
}* tree;

/*This test is not suitable for ARTMC itself. Only tests some features of C2ARTMC*/

void dfs(tree x) {
    tree y,z;
    while (x && y && x->right != y->right || y->right != z->right->right->right) {
        while (!x || !y || x->right->right->parrent != y->parrent->left && y->right->data) {
            y=x->right;
        }
    }
}

