module Demux_LFSR_LED_Top(
    input i_Clk,
    input i_Switch_1,
    input i_Switch_2,
    output o_LED_1,
    output o_LED_2,
    output o_LED_3,
    output o_LED_4
);
    wire w_cycled;
    reg r_toggle = 1'b0;

    //LFSR 23 bit instance
    LFSR LFSR_inst (
        .i_Clk(i_Clk),
        .o_cycled(w_cycled)
    );
    
    always @(posedge i_Clk)begin
        if (w_cycled)begin
            r_toggle <= !r_toggle;
        end 
    end


    //Demux instance
    Demux_1_4 Demux_Inst(
        .i_data(r_toggle),
        .i_select_0(i_Switch_1),
        .i_select_1(i_Switch_2),
        .o_data_0(o_LED_1),
        .o_data_1(o_LED_2),
        .o_data_2(o_LED_3),
        .o_data_3(o_LED_4)
    );

endmodule
