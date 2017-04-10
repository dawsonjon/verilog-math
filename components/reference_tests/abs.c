#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    float f;
    int i;
    unsigned int a;

    infa = fopen("stim/abs_a", "r");
    outf = fopen("stim/abs_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        i = *(int*)&a & 0x7fffffff;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
