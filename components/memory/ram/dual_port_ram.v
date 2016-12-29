module dual_port_ram(clk_1, data_in_1, data_out_1, address_1, write_enable_1, clk_2, data_in_2, data_out_2, address_2, data_in_2, write_enable_2);

  parameter depth = 1024;
  parameter data_width = 8;
  parameter address_width = 8;

  output reg [data_width-1:0] data_out_1;
  input [data_width-1:0] data_in_1;
  output reg [data_width-1:0] data_out_2;
  input [data_width-1:0] data_in_2;
  input [address_width-1:0] address_1;
  input [address_width-1:0] address_2;
  input write_enable_1, write_enable_2, clk_1, clk_2;
 
  reg [data_width-1:0] mem [depth-1:0];

  always @(posedge clk_1) begin
    if (write_enable_1)
        mem[address_1] <= data_in_1;
  end
 
  always @(posedge clk_1) begin
     data_out_1 <= mem[address_1];
  end

  always @(posedge clk_2) begin
    if (write_enable_2)
        mem[address_2] <= data_in_2;
  end
 
  always @(posedge clk_2) begin
     data_out_2 <= mem[address_2];
  end
        
endmodule
