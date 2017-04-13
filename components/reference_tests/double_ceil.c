#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    long long int i;
    long long unsigned int a;

    infa = fopen("stim/double_ceil_a", "r");
    outf = fopen("stim/double_ceil_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        f = *(double*)&a;
        f = ceil(f);
        i = *(long long int*)&f;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
