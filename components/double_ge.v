//This file was automatically generated by the python 'pipeliner' script
//This module has a latency of 2 clocks
module dq (clk, q, d);
  input  clk;
  input  [width-1:0] d;
  output [width-1:0] q;
  parameter width=8;
  parameter depth=2;
  integer i;
  reg [width-1:0] delay_line [depth-1:0];
  always @(posedge clk) begin
    delay_line[0] <= d;
    for(i=1; i<depth; i=i+1) begin
      delay_line[i] <= delay_line[i-1];
    end
  end
  assign q = delay_line[depth-1];
endmodule

module double_ge(clk, double_ge_a, double_ge_b, double_ge_z);
  input clk;
  input [63:0] double_ge_a;
  input [63:0] double_ge_b;
  output [0:0] double_ge_z;
  wire [0:0] s_0;
  wire [0:0] s_1;
  wire [0:0] s_2;
  wire [0:0] s_3;
  wire [0:0] s_4;
  wire [0:0] s_5;
  wire [0:0] s_6;
  wire [0:0] s_7;
  wire [0:0] s_8;
  wire [63:0] s_9;
  wire [0:0] s_10;
  wire [0:0] s_11;
  wire [63:0] s_12;
  wire [0:0] s_13;
  wire [0:0] s_14;
  wire [0:0] s_15;
  wire [11:0] s_16;
  wire [10:0] s_17;
  wire [10:0] s_18;
  wire [10:0] s_19;
  wire [10:0] s_20;
  wire [9:0] s_21;
  wire [0:0] s_22;
  wire [10:0] s_23;
  wire [11:0] s_24;
  wire [10:0] s_25;
  wire [10:0] s_26;
  wire [10:0] s_27;
  wire [10:0] s_28;
  wire [9:0] s_29;
  wire [0:0] s_30;
  wire [10:0] s_31;
  wire [0:0] s_32;
  wire [0:0] s_33;
  wire [10:0] s_34;
  wire [0:0] s_35;
  wire [51:0] s_36;
  wire [51:0] s_37;
  wire [0:0] s_38;
  wire [0:0] s_39;
  wire [0:0] s_40;
  wire [10:0] s_41;
  wire [0:0] s_42;
  wire [51:0] s_43;
  wire [51:0] s_44;
  wire [0:0] s_45;
  wire [0:0] s_46;
  wire [56:0] s_47;
  wire [56:0] s_48;
  wire [52:0] s_49;
  wire [52:0] s_50;
  wire [0:0] s_51;
  wire [0:0] s_52;
  wire [0:0] s_53;
  wire [52:0] s_54;
  wire [0:0] s_55;
  wire [0:0] s_56;
  wire [0:0] s_57;
  wire [1:0] s_58;
  wire [56:0] s_59;
  wire [56:0] s_60;
  wire [56:0] s_61;
  wire [56:0] s_62;
  wire [52:0] s_63;
  wire [1:0] s_64;
  wire [11:0] s_65;
  wire [11:0] s_66;
  wire [11:0] s_67;
  wire [0:0] s_68;
  wire [56:0] s_69;
  wire [56:0] s_70;
  wire [56:0] s_71;
  wire [0:0] s_72;
  wire [0:0] s_73;
  wire [56:0] s_74;
  wire [56:0] s_75;
  wire [56:0] s_76;
  wire [56:0] s_77;
  wire [56:0] s_78;
  wire [56:0] s_79;
  wire [56:0] s_80;
  wire [56:0] s_81;
  wire [56:0] s_82;
  wire [0:0] s_83;
  wire [0:0] s_84;
  wire [0:0] s_85;
  wire [0:0] s_86;
  wire [0:0] s_87;
  wire [0:0] s_88;
  wire [10:0] s_89;
  wire [0:0] s_90;
  wire [51:0] s_91;
  wire [0:0] s_92;
  wire [0:0] s_93;
  wire [0:0] s_94;
  wire [0:0] s_95;
  wire [10:0] s_96;
  wire [0:0] s_97;
  wire [51:0] s_98;

  assign s_0 = s_1 & s_92;
  assign s_1 = s_2 & s_85;
  assign s_2 = ~s_3;
  assign s_3 = s_73?s_4:s_5;
  assign s_4 = 1'd0;
  dq #(1, 2) dq_s_5 (clk, s_5, s_6);
  assign s_6 = s_46?s_7:s_45;
  assign s_7 = s_13?s_8:s_10;
  assign s_8 = s_9[63];
  assign s_9 = double_ge_a;
  assign s_10 = ~s_11;
  assign s_11 = s_12[63];
  assign s_12 = double_ge_b;
  assign s_13 = s_14 & s_38;
  assign s_14 = s_15 | s_32;
  assign s_15 = $signed(s_16) > $signed(s_24);
  assign s_16 = $signed(s_17);
  assign s_17 = s_22?s_18:s_19;
  assign s_18 = -11'd1022;
  assign s_19 = s_20 - s_21;
  assign s_20 = s_9[62:52];
  assign s_21 = 10'd1023;
  assign s_22 = s_19 == s_23;
  assign s_23 = -11'd1023;
  assign s_24 = $signed(s_25);
  assign s_25 = s_30?s_26:s_27;
  assign s_26 = -11'd1022;
  assign s_27 = s_28 - s_29;
  assign s_28 = s_12[62:52];
  assign s_29 = 10'd1023;
  assign s_30 = s_27 == s_31;
  assign s_31 = -11'd1023;
  assign s_32 = s_33 & s_35;
  assign s_33 = s_19 == s_34;
  assign s_34 = 11'd1024;
  assign s_35 = s_36 == s_37;
  assign s_36 = s_9[51:0];
  assign s_37 = 52'd0;
  assign s_38 = ~s_39;
  assign s_39 = s_40 & s_42;
  assign s_40 = s_27 == s_41;
  assign s_41 = 11'd1024;
  assign s_42 = s_43 == s_44;
  assign s_43 = s_12[51:0];
  assign s_44 = 52'd0;
  assign s_45 = s_13?s_10:s_8;
  assign s_46 = s_47 >= s_59;
  assign s_47 = s_48 << s_58;
  assign s_48 = s_49;
  assign s_49 = s_13?s_50:s_54;
  assign s_50 = {s_51,s_36};
  assign s_51 = s_22?s_52:s_53;
  assign s_52 = 1'd0;
  assign s_53 = 1'd1;
  assign s_54 = {s_55,s_43};
  assign s_55 = s_30?s_56:s_57;
  assign s_56 = 1'd0;
  assign s_57 = 1'd1;
  assign s_58 = 2'd3;
  assign s_59 = s_60 | s_68;
  assign s_60 = s_61 >> s_65;
  assign s_61 = s_62 << s_64;
  assign s_62 = s_63;
  assign s_63 = s_13?s_54:s_50;
  assign s_64 = 2'd3;
  assign s_65 = s_66 - s_67;
  assign s_66 = s_13?s_16:s_24;
  assign s_67 = s_13?s_24:s_16;
  assign s_68 = s_69 != s_72;
  assign s_69 = s_61 << s_70;
  assign s_70 = s_71 - s_65;
  assign s_71 = 57'd57;
  assign s_72 = 1'd0;
  assign s_73 = s_74 == s_84;
  dq #(57, 1) dq_s_74 (clk, s_74, s_75);
  assign s_75 = s_76 + s_78;
  dq #(57, 1) dq_s_76 (clk, s_76, s_77);
  assign s_77 = s_46?s_47:s_59;
  dq #(57, 1) dq_s_78 (clk, s_78, s_79);
  assign s_79 = s_83?s_80:s_81;
  assign s_80 = s_46?s_59:s_47;
  assign s_81 = s_82 - s_80;
  assign s_82 = 57'd0;
  assign s_83 = s_8 == s_10;
  assign s_84 = 1'd0;
  dq #(1, 2) dq_s_85 (clk, s_85, s_86);
  assign s_86 = ~s_87;
  assign s_87 = s_88 & s_90;
  assign s_88 = s_19 == s_89;
  assign s_89 = 11'd1024;
  assign s_90 = s_36 != s_91;
  assign s_91 = 52'd0;
  dq #(1, 2) dq_s_92 (clk, s_92, s_93);
  assign s_93 = ~s_94;
  assign s_94 = s_95 & s_97;
  assign s_95 = s_27 == s_96;
  assign s_96 = 11'd1024;
  assign s_97 = s_43 != s_98;
  assign s_98 = 52'd0;
  assign double_ge_z = s_0;
endmodule