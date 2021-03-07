def mk_fifo(filename, depth, width):

    of = open(filename, "w")
    of.write(
        """module fifo (clk, rst, data_in, data_out, data_in_stb, data_in_ack, data_out_stb, data_out_ack);

    parameter width = %u;
    parameter depth = %u;
    parameter address_bits = %u;

    input clk;
    input rst;

    input [width-1:0] data_in;
    input data_in_stb;
    output data_in_ack;

    output [width-1:0] data_out;
    output data_out_stb;
    input data_out_ack;

    reg s_output_stb;
    wire s_input_ack;
    wire full;
    wire empty;
    wire read;
    wire write;
    reg [address_bits-1:0] a_out;
    reg [address_bits-1:0] a_in;
    reg [width-1:0] memory [0:depth-1];

    always @ (posedge clk) begin
        if (write) begin
          memory[a_in] <= data_in;
        end

        if (read) begin
          data_out <= memory[a_out];
        end
    end

    always @ (posedge clk) begin

        s_output_stb <= 0;
        if (read) begin
          //data is available on clock following read
          s_output_stb <= 1;
          if (a_out == (depth - 1)) begin
            a_out <= 0;
          end else begin
            a_out <= a_out + 1;
          end
        end

        //if data has not been read, extend strobe
        if (s_output_stb &~ output_ack) begin
          s_output_stb <= 1;
        end

        if (write) begin
          if (a_in == (depth - 1)) begin
            a_in <= 0;
          end else begin
            a_in <= a_in + 1;
          end
        end

        if (rst) begin
          a_out <= 0;
          a_in <= 0;
          s_output_stb <= 0;
        end

    end 

    assign full = (a_out-1 == a_in ) | ((a_out == 0) & (a_in == depth - 1));
    assign empty = (a_out == a_in);
    assign s_input_ack = ~full;
    assign output_stb = s_output_stb;
    assign input_ack = s_input_ack;
    assign write = s_input_ack & input_stb;
    assign read  = (~s_output_stb | output_ack) & ~empty;


endmodule"""
        % (width, depth, int(round(ceil(math.log2(depth)))))
    )
