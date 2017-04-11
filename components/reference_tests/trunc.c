#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    float f, f_int_part;
    double int_part;
    int i;
    unsigned int a;

    infa = fopen("stim/trunc_a", "r");
    outf = fopen("stim/trunc_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        f = *(float*)&a;
        modf((double)f, &int_part);
        f_int_part = int_part;
        i = *(int*)&f_int_part;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
