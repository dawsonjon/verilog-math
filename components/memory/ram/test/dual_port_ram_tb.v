module dual_port_ram_tb;

wire [31:0] data_out_1;
wire [31:0] data_in_1;
wire [31:0] address_1;
wire [31:0] we_1;
wire [31:0] data_out_2;
wire [31:0] data_in_2;
wire [31:0] address_2;
wire [31:0] we_2;
reg clk, rst;

main_0 tester (

    .clk(clk),
    .rst(rst),

    .output_address_1(address_1),
    .output_address_1_ack(1'b1),

    .output_we_1(we_1),
    .output_we_1_ack(1'b1),

    .output_data_in_1(data_in_1),
    .output_data_in_1_ack(1'b1),

    .input_data_out_1(data_out_1),
    .input_data_out_1_stb(1'b1),

    .output_address_2(address_2),
    .output_address_2_ack(1'b1),

    .output_we_2(we_2),
    .output_we_2_ack(1'b1),

    .output_data_in_2(data_in_2),
    .output_data_in_2_ack(1'b1),

    .input_data_out_2(data_out_2),
    .input_data_out_2_stb(1'b1)

);
    
dual_port_ram #(

     .address_width(32),
     .data_width(32),
     .depth(256)

) uut (

    .data_in_1(data_in_1), 
    .data_out_1(data_out_1), 
    .address_1(address_1), 
    .write_enable_1(we_1[0]), 
    .data_in_2(data_in_2), 
    .data_out_2(data_out_2), 
    .address_2(address_2), 
    .write_enable_2(we_2[0]), 
    .clk_1(clk), 
    .clk_2(clk)

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
