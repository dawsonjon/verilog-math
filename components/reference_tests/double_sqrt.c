#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;

    infa = fopen("stim/double_sqrt_a", "r");
    outf = fopen("stim/double_sqrt_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = sqrt(*(double*)&a);
        i = *(long long int*)&f;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
