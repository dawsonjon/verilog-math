#include "stdio.h"
#include <math.h>

void main(){


    FILE *infa;
    FILE *infb;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/double_min_a", "r");
    infb = fopen("stim/double_min_b", "r");
    outf = fopen("stim/double_min_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        if(fscanf(infb, "%llu", &b) == EOF) break;
        f = *(double*)&a < *(double*)&b ? *(double*)&a : *(double*)&b;
        if(isnan(*(double*)&a)) f = *(double*)&a;
        if(isnan(*(double*)&b)) f = *(double*)&b;
        i = *(long long int*)&f;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(infb);
    fclose(outf);


}
