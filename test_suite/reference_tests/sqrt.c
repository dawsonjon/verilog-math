#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    float f;
    int i;
    unsigned int a;

    infa = fopen("stim/sqrt_a", "r");
    outf = fopen("stim/sqrt_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        f = sqrt(*(float*)&a);
        i = *(int*)&f;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
