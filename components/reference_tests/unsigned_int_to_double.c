#include "stdio.h"

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    unsigned long long int i;
    unsigned long long int a;
    unsigned long long int b;

    infa = fopen("stim/unsigned_int_to_double_a", "r");
    outf = fopen("stim/unsigned_int_to_double_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = (double)(long long unsigned int)a;
        i = *((long long int*)&f);
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
