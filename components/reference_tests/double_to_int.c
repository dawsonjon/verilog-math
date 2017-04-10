#include "stdio.h"

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/double_to_int_a", "r");
    outf = fopen("stim/double_to_int_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = *(double*)&a;
        i = f;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
