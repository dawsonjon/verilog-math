module dual_port_ram(data_out, address, data_in, write_enable, clk);

  parameter depth 1024;
  parameter data_width 8;
  parameter address_width 8;

  output[data_width-1:0] data_out;
  input [data_width-1:0] data_in;
  input [address_width-1:0] address;
  input write_enable, clk;
 
  reg [data_width-1:0] data_out;
  reg [data_width-1:0] mem [127:0];

  always @(posedge clk) begin
    if (write_enable) mem[address] <= data_in;
  end
 
  always @(posedge clk) begin
     data_out <= mem[address];
  end
        
endmodule
