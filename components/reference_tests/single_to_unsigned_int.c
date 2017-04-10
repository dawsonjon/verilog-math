#include "stdio.h"

void main(){


    FILE *infa;
    FILE *outf;

    float f;
    unsigned int i;
    unsigned int a;
    unsigned int b;

    infa = fopen("stim/single_to_unsigned_int_a", "r");
    outf = fopen("stim/single_to_unsigned_int_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        f = *(float*)&a;
        i = f;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
