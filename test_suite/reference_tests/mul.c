#include "stdio.h"

void main(){


    FILE *infa;
    FILE *infb;
    FILE *outf;

    float f;
    int i;
    unsigned int a;
    unsigned int b;

    infa = fopen("stim/mul_a", "r");
    infb = fopen("stim/mul_b", "r");
    outf = fopen("stim/mul_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        if(fscanf(infb, "%u", &b) == EOF) break;
        f = *(float*)&a * *(float*)&b;
        i = *(int*)&f;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(infb);
    fclose(outf);


}
