/*
Basic 4 Shift register 
*/
module Basic_Delay_Shift(
    input i_data_to_delay,
    input i_Clk
);
    reg [3:0] r_shift; //series of flip flops where ouytput of one flip flop is connected to input of next
    //each additional flip-flop adds another clock cycle delay
    always @(posedge i_Clk) begin
        r_shift[0] <= i_data_to_delay;
        r_shift[3:1] <= r_shift[2:0];
        /*
        Above equivalent to saying 
        r_shift[1]<=r_shift[0];
        r_shift[2]<=r_shift[1];
        r_shift[3]<=r_shift[2];
        */
    end


endmodule