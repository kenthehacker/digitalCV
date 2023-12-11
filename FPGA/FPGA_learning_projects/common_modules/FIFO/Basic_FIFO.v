module FIFO #(parameter WIDTH = 8, parameter LEVEL = 4)
(
    input i_Wr_Clk,
    input i_Wr_DV,
    input [WIDTH-1:0]i_Wr_Data,
    input [LEVEL-1:0]i_AF_Level,
    output o_AF_Flag,
    output o_Full,
    input i_Rd_Clk,
    input i_Rd_En,
    input [LEVEL-1:0] i_AE_Level,
    output o_Rd_DV,
    output [WIDTH-1:0] o_Rd_Data,
    output o_AE_Flag,
    output o_Empty
);
    parameter DEPTH = 128; //128 bits deep fifo
    reg [WIDTH-1:0] fifo[0:DEPTH-1];
    reg [9:0] count; //number of storage locations/depth of the fifo being tracked here
    //read & write ptrs
    reg [LEVEL-1:0] rd_ptr;
    reg [LEVEL-1:0] wr_ptr;

    //write
    always @(posedge i_Wr_Clk)begin
        if (i_Wr_DV && o_Full && ~i_Rd_En)begin
            fifo[wr_ptr] <= i_Wr_Data;
            wr_ptr<= (wr_ptr == DEPTH-1)? 0 : wr_ptr+1;
            if (!o_Full)count<=count+1;
        end 
    end 

    //read
    always @(posedge i_Rd_Clk) begin
        if (i_Rd_En && ~i_Write_DV && !o_Empty)begin 
            o_Rd_Data <= fifo[rd_ptr];
            rd_ptr <= (rd_ptr==DEPTH-1) ? 0 : rd_ptr+1;
            if (!o_Empty) count<= count+1;
        end 
    end 

    //flag update
    assign o_Full = (count >= DEPTH || (count == DEPTH-1 && i_Wr_DV && !i_Rd_En));
    assign o_Empty = (count == 0);
    assign o_AF_Flag = (count>DEPTH-i_AF_Level);
    assign o_AE_Flag = (count<i_AE_Level);
endmodule
