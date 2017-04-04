#include "stdio.h"

void main(){


    FILE *infa;
    FILE *infb;
    FILE *outf;

    int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/double_ne_a", "r");
    infb = fopen("stim/double_ne_b", "r");
    outf = fopen("stim/double_ne_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        if(fscanf(infb, "%llu", &b) == EOF) break;
        i = *(double*)&a != *(double*)&b;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(infb);
    fclose(outf);


}
