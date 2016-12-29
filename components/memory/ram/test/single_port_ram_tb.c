address = output("address");
we = output("we");
data_in = output("data_in");
data_out = input("data_out");

void main(){
    int i;

    fputc(we, 0);

    for(i=0; i<256; i++){
        fputc(i, address);
        fputc(i, data_in);
        fputc(1, we);
        fputc(0, we);
        report(i);
    }

    for(i=0; i<256; i++){
        report(i);
        fputc(i, address);
        assert(fgetc(data_out)==i);
    }

}
