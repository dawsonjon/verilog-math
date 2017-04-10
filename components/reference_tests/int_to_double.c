#include "stdio.h"

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/int_to_double_a", "r");
    outf = fopen("stim/int_to_double_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = (double)(long long int)a;
        i = *((long long int*)&f);
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
