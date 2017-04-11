#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    double int_part;
    long long int i;
    unsigned long long int a;

    infa = fopen("stim/double_trunc_a", "r");
    outf = fopen("stim/double_trunc_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = *(double*)&a;
        modf(f, &int_part);
        i = *(long long int*)&int_part;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
