#include "stdio.h"

void main(){


    FILE *infa;
    FILE *infb;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/double_div_a", "r");
    infb = fopen("stim/double_div_b", "r");
    outf = fopen("stim/double_div_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        if(fscanf(infb, "%llu", &b) == EOF) break;
        f = *(double*)&a / *(double*)&b;
        i = *(long long int*)&f;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(infb);
    fclose(outf);


}
