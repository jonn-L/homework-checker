/*
CH-230-A
a5_p6.c 
Merey Yessengaliyeva 
myessengal@jacobs-university.de
*/


#include <stdio.h>
#include <stdlib.h>

//function to count values by pointer
int count(float *array){
    int id = 0;
    while(1){
        if((*(array)+id)>0){
            id++;
        }
        else{
            break;
        }
    }
    return id;
}

int main()
{
    //declared variables, memory allocated and called function
    int n,i;
    scanf("%d",&n);
    float *array;
    array=(float*)malloc(sizeof(float)*n);


    //for loop to scanf values until we reach n value we set.
    for (i=0; i<n; i++){
        scanf("%f",array+i);
    }
    puts("geni");
    printf("Before the first negative value: %d elements",count(array));
    return 0;
}