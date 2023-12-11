module Ram_2Port #(parameter WIDTH = 16, DEPTH = 256)
(
    input i_Write_Clk,
    input [$clog2(DEPTH)-1 : 0] i_Write_Addr,
    input i_Write_DV,
    input [DEPTH-1 : 0] i_Write_Data,
    input i_Read_Clk,
    input [$clog2(DEPTH)-1 : 0] i_Read_Addr,
    input i_Read_En,
    output o_Read_DV,
    output [DEPTH-1 : 0] o_Read_Data
);
    reg [WIDTH-1 : 0] r_ram [DEPTH-1 : 0];
    
    always @(posedge i_Write_Clk)begin
        if (i_Write_DV)begin
            r_ram[i_Write_Addr] <= i_Write_Data;
        end 
    end

    always @(posedge i_Read_Clk)begin
        o_Read_Data <= r_ram[i_Read_Addr];
        o_Read_DV <= i_Read_En;
    end 

endmodule
