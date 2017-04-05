#include "stdio.h"

void main(){


    FILE *infa;
    FILE *outf;

    float f;
    int i;
    unsigned int a;
    unsigned int b;

    infa = fopen("stim/int_to_single_a", "r");
    outf = fopen("stim/int_to_single_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        f = (float)(int)a;
        i = *((int*)&f);
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
