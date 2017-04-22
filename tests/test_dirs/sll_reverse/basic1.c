#include <stdlib.h>

typedef struct Liste1 {
  struct Liste1 *next;
  int data;
}* Liste;

Liste reverse(Liste x){
  Liste y, t;
  t = NULL;
  while(x != NULL){
    y = x;
    x = x->next;
    y->next = t;
    t = y;
  }
  return y;
}
