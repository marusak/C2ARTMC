#include <stdlib.h>

typedef struct tree1 {
	int data;
	struct tree1 *left;
	struct tree1 *right;
	struct tree1 *parrent;
}* tree;

/* We suppose, that the data structure is on the beginning pointed by variable x */

void dfs(tree x) {
	tree y;
	while (x != NULL) {
		y=x->left;
		if ((y != NULL) && (y->data == 0))
			x=y;
		else {
			y=x->right;
			if ((y != NULL) && (y->data == 0))
				x=y;
			else {
				x->data=1;
				x=x->parrent;
			}
		}
	}
}

