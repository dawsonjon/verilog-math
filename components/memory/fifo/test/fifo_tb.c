address_1 = output("address_1");
we_1 = output("we_1");
data_in_1 = output("data_in_1");
data_out_1 = input("data_out_1");

address_2 = output("address_2");
we_2 = output("we_2");
data_in_2 = output("data_in_2");
data_out_2 = input("data_out_2");

void main(){
    int i;

    fputc(0, we_1);
    fputc(0, we_2);

    for(i=0; i<256; i++){
        fputc(i, address_1);
        fputc(i, data_in_1);
        fputc(1, we_1);
        fputc(0, we_1);
        report(i);
    }

    for(i=0; i<256; i++){
        report(i);
        fputc(i, address_2);
        assert(fgetc(data_out_2)==i);
    }

    for(i=0; i<256; i++){
        fputc(i, address_2);
        fputc(~i, data_in_2);
        fputc(1, we_2);
        fputc(0, we_2);
        report(i);
    }

    for(i=0; i<256; i++){
        report(i);
        fputc(i, address_1);
        assert(fgetc(data_out_1)==~i);
    }

}
