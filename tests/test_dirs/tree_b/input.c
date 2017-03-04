#include <stdlib.h>
#include <stdbool.h>
#define WHITE 1
#define TREE 2
#define BLUE 3

typedef struct tree1 {
    int data;
    struct tree1 *left;
    struct tree1 *right;
}* tree;

tree root, n, aux;

int main()
{
    root = malloc(sizeof(TREE));
    root->left = NULL;
    root->right = NULL;
    root->data = WHITE;

    // create an arbitrary white tree
    while (*)
    {
        n = root;
        while (n->left != NULL || n->right != NULL)
        {
            if (n->left != NULL && n->right != NULL && *)
                n = n->left;
            else if (n->right != NULL)
                n = n->right;
            else
                n = n->left;
        }


        // create a node
        if (*)
        {
            aux = malloc(sizeof(TREE));
            aux->left = NULL;
            aux->right = NULL;
            aux->data = WHITE;
            n->left=aux;
        }
        // else
        if (*)
        {
            aux = malloc(sizeof(TREE));
            aux->left = NULL;
            aux->right = NULL;
            aux->data = WHITE;
            n->right=aux;
        }
    }

    n = root;
    // Choose one node to mark it blue
    while (*)
    {
        if (*)
            n = n->left;
        else
            n= n->right;
        if (n == NULL)
            return 1;
    }

    n->data = BLUE;

    // check the invariant
    n = root;

    while (n->data != BLUE)
    {
        if (*)
            n = n-> left;
        else
            n = n-> right;
        if (n == NULL)
            return 1;
    }

    // look for another blue guy
    while (true)
    {
        if (*)
            n = n-> left;
        else
            n = n-> right;
        if (n == NULL)
            return 1;

        if (n->data == BLUE)
            return 1;
    }


    return 0;
}
