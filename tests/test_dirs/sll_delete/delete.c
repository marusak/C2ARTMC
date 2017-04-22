#include <stdlib.h>

typedef struct Liste1 {
  struct Liste1 *next;
  int data;
}* Liste;

Liste delete(Liste x,int delval){
    Liste elem, prev, temp;
    elem = x;
    prev = NULL;
    temp = NULL;
    while(elem != NULL){
        if(elem->data == delval){
            if(prev==NULL){
                x=elem->next;
            }
            else{
                temp=elem->next;
                prev->next=temp;
            }
            elem->next=NULL;
            free(elem);
            return x;
        }
        prev=elem;
        elem=elem->next;
    }
    return x;
}
