#include "stdio.h"
#include <math.h>

void main(){


    FILE *infa;
    FILE *infb;
    FILE *outf;

    float f;
    int i;
    unsigned int a;
    unsigned int b;

    infa = fopen("stim/single_min_a", "r");
    infb = fopen("stim/single_min_b", "r");
    outf = fopen("stim/single_min_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        if(fscanf(infb, "%u", &b) == EOF) break;
        f = *(float*)&a < *(float*)&b ? *(float*)&a : *(float*)&b;
        if(isnan(*(float*)&a)) f = *(float*)&a;
        if(isnan(*(float*)&b)) f = *(float*)&b;
        i = *(int*)&f;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(infb);
    fclose(outf);


}
