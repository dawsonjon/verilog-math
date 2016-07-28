module uut_tb;
  reg clk;
  reg [31:0] a;
  reg [31:0] b;
  wire [31:0] z;
  integer a_file;
  integer b_file;
  integer z_file;
  integer a_count;
  integer b_count;
  integer z_count;

  uut uut1 (clk, a, b, z);
  initial
  begin
    z_file = $fopen("z");
    a_file = $fopenr("a");
    b_file = $fopenr("b");
  end

  initial
  begin
    #10080 $finish;
  end

  initial
  begin
    clk <= 1'b0;
    while (1) begin
      #5 clk <= ~clk;
    end
  end

  always @ (posedge clk)
  begin
    $fdisplay(z_file, "%d", z);
    #0 a_count = $fscanf(a_file, "%d\n", a);
    #0 b_count = $fscanf(b_file, "%d\n", b);
  end
endmodule
