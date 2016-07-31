module uut_tb;
  reg clk;
  reg [31:0] a;
  reg [31:0] b;
  wire [8:0] a_e0;
  wire [8:0] b_e1;
  wire [47:0] a_m2;
  wire [47:0] b_m3;
  wire [0:0] a_s4;
  wire [0:0] b_s5;
  wire [47:0] z_m6;
  wire [8:0] z_e7;
  wire [8:0] shift_amount8;
  wire [47:0] m9;
  wire [8:0] e10;
  wire [8:0] e11;
  wire [47:0] z_m12;
  wire [8:0] z_e13;
  wire [23:0] z_m14;
  wire [23:0] z_m15;
  wire [8:0] z_e16;
  wire [0:0] z_s17;
  wire [7:0] e_max18;
  wire [0:0] overflow19;
  wire [0:0] z_inf20;
  wire [0:0] z_nan21;
  wire [31:0] result22;
  wire [31:0] z;
  integer a_file;
  integer b_file;
  integer a_e0_file;
  integer b_e1_file;
  integer a_m2_file;
  integer b_m3_file;
  integer a_s4_file;
  integer b_s5_file;
  integer z_m6_file;
  integer z_e7_file;
  integer shift_amount8_file;
  integer m9_file;
  integer e10_file;
  integer e11_file;
  integer z_m12_file;
  integer z_e13_file;
  integer z_m14_file;
  integer z_m15_file;
  integer z_e16_file;
  integer z_s17_file;
  integer e_max18_file;
  integer overflow19_file;
  integer z_inf20_file;
  integer z_nan21_file;
  integer result22_file;
  integer z_file;
  integer a_count;
  integer b_count;
  integer a_e0_count;
  integer b_e1_count;
  integer a_m2_count;
  integer b_m3_count;
  integer a_s4_count;
  integer b_s5_count;
  integer z_m6_count;
  integer z_e7_count;
  integer shift_amount8_count;
  integer m9_count;
  integer e10_count;
  integer e11_count;
  integer z_m12_count;
  integer z_e13_count;
  integer z_m14_count;
  integer z_m15_count;
  integer z_e16_count;
  integer z_s17_count;
  integer e_max18_count;
  integer overflow19_count;
  integer z_inf20_count;
  integer z_nan21_count;
  integer result22_count;
  integer z_count;

  uut uut1 (clk, a, b, a_e0, b_e1, a_m2, b_m3, a_s4, b_s5, z_m6, z_e7, shift_amount8, m9, e10, e11, z_m12, z_e13, z_m14, z_m15, z_e16, z_s17, e_max18, overflow19, z_inf20, z_nan21, result22, z);
  initial
  begin
    $dumpfile("test.vcd");
    $dumpvars(0,uut_tb);
    a_e0_file = $fopen("a_e0");
    b_e1_file = $fopen("b_e1");
    a_m2_file = $fopen("a_m2");
    b_m3_file = $fopen("b_m3");
    a_s4_file = $fopen("a_s4");
    b_s5_file = $fopen("b_s5");
    z_m6_file = $fopen("z_m6");
    z_e7_file = $fopen("z_e7");
    shift_amount8_file = $fopen("shift_amount8");
    m9_file = $fopen("m9");
    e10_file = $fopen("e10");
    e11_file = $fopen("e11");
    z_m12_file = $fopen("z_m12");
    z_e13_file = $fopen("z_e13");
    z_m14_file = $fopen("z_m14");
    z_m15_file = $fopen("z_m15");
    z_e16_file = $fopen("z_e16");
    z_s17_file = $fopen("z_s17");
    e_max18_file = $fopen("e_max18");
    overflow19_file = $fopen("overflow19");
    z_inf20_file = $fopen("z_inf20");
    z_nan21_file = $fopen("z_nan21");
    result22_file = $fopen("result22");
    z_file = $fopen("z");
    a_file = $fopenr("a");
    b_file = $fopenr("b");
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
    $fdisplay(a_e0_file, "%d", a_e0);
    $fdisplay(b_e1_file, "%d", b_e1);
    $fdisplay(a_m2_file, "%d", a_m2);
    $fdisplay(b_m3_file, "%d", b_m3);
    $fdisplay(a_s4_file, "%d", a_s4);
    $fdisplay(b_s5_file, "%d", b_s5);
    $fdisplay(z_m6_file, "%d", z_m6);
    $fdisplay(z_e7_file, "%d", z_e7);
    $fdisplay(shift_amount8_file, "%d", shift_amount8);
    $fdisplay(m9_file, "%d", m9);
    $fdisplay(e10_file, "%d", e10);
    $fdisplay(e11_file, "%d", e11);
    $fdisplay(z_m12_file, "%d", z_m12);
    $fdisplay(z_e13_file, "%d", z_e13);
    $fdisplay(z_m14_file, "%d", z_m14);
    $fdisplay(z_m15_file, "%d", z_m15);
    $fdisplay(z_e16_file, "%d", z_e16);
    $fdisplay(z_s17_file, "%d", z_s17);
    $fdisplay(e_max18_file, "%d", e_max18);
    $fdisplay(overflow19_file, "%d", overflow19);
    $fdisplay(z_inf20_file, "%d", z_inf20);
    $fdisplay(z_nan21_file, "%d", z_nan21);
    $fdisplay(result22_file, "%d", result22);
    $fdisplay(z_file, "%d", z);
    #0 a_count = $fscanf(a_file, "%d\n", a);
    #0 b_count = $fscanf(b_file, "%d\n", b);
  end
endmodule
