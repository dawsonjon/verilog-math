#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    double f;
    long long int i;
    unsigned long long int a;

    infa = fopen("stim/double_abs_a", "r");
    outf = fopen("stim/double_abs_z_expected", "w");

    while(1){
        if(fscanf(infa, "%llu", &a) == EOF) break;
        i = *(long long int*)&a & 0x7fffffffffffffffll;
        fprintf(outf, "%llu\n", i);
    }

    fclose(infa);
    fclose(outf);


}
