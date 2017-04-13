#include <stdio.h>
#include <math.h>

void main(){


    FILE *infa;
    FILE *outf;

    float f;
    int i;
    unsigned int a;

    infa = fopen("stim/floor_a", "r");
    outf = fopen("stim/floor_z_expected", "w");

    while(1){
        if(fscanf(infa, "%u", &a) == EOF) break;
        f = *(float*)&a;
        f = floor(f);
        i = *(int*)&f;
        fprintf(outf, "%u\n", i);
    }

    fclose(infa);
    fclose(outf);


}
