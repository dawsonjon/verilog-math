module lz_tb;
  reg clk;
  reg [2:0] a;
  wire [1:0] msb;
  wire [1:0] lsb;
  wire [0:0] msbs_are_zero;
  wire [0:0] lsbs_are_zero;
  wire [2:0] z;
  integer a_file;
  integer msb_file;
  integer lsb_file;
  integer msbs_are_zero_file;
  integer lsbs_are_zero_file;
  integer z_file;
  integer a_count;
  integer msb_count;
  integer lsb_count;
  integer msbs_are_zero_count;
  integer lsbs_are_zero_count;
  integer z_count;

  lz lz1 (clk, a, msb, lsb, msbs_are_zero, lsbs_are_zero, z);
  initial
  begin
    msb_file = $fopen("stim/msb");
    lsb_file = $fopen("stim/lsb");
    msbs_are_zero_file = $fopen("stim/msbs_are_zero");
    lsbs_are_zero_file = $fopen("stim/lsbs_are_zero");
    z_file = $fopen("stim/z");
    a_file = $fopenr("stim/a");
  end

  initial
  begin
    #50 $finish;
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
    $fdisplay(msb_file, "%d", msb);
    $fdisplay(lsb_file, "%d", lsb);
    $fdisplay(msbs_are_zero_file, "%d", msbs_are_zero);
    $fdisplay(lsbs_are_zero_file, "%d", lsbs_are_zero);
    $fdisplay(z_file, "%d", z);
    #0 a_count = $fscanf(a_file, "%d\n", a);
  end
endmodule
