module single_port_ram_tb;

wire [31:0] data_out;
wire [31:0] data_in;
wire [31:0] address;
wire [31:0] we;
reg clk, rst;

main_0 tester (
    .input_data_out(data_out),
    .input_data_out_stb(1'b1),

    .clk(clk),
    .rst(rst),

    .output_address(address),
    .output_address_ack(1'b1),

    .output_we(we),
    .output_we_ack(1'b1),

    .output_data_in(data_in),
    .output_data_in_ack(1'b1)
);
    
single_port_ram #(

     .address_width(32),
     .data_width(32),
     .depth(256)

) uut (

    .data_out(data_out), 
    .address(address), 
    .data_in(data_in), 
    .write_enable(we[0]), 
    .clk(clk)

);

initial begin
    clk = 0;
    rst = 1;
end

always begin 
    #5  clk =  ! clk; 
end

initial begin 
    #50  rst = 0; 
end

initial begin 
    #1000000  $finish; 
end

initial begin
    $dumpfile ("dump.vcd"); 
    $dumpvars; 
end 

endmodule
