module LFSR(
    input i_Clk,
    output o_cycled
);
    reg [22:0] r_LFSR;
    initial begin
        r_LFSR = 23'b1;
    end
    //in initial block so it only runs once
    wire w_XNOR;
    always @(posedge i_Clk)begin
        r_LFSR <= {r_LFSR[21:0], w_XNOR};
    end 
    assign w_XNOR = r_LFSR[22] ^ ~r_LFSR[21];
     
    assign o_cycled = (r_LFSR == 23'b1); 

endmodule