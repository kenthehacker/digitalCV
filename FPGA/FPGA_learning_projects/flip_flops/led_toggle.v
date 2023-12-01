/*
Toggle state of LED each time swich is released
if LED was off before switch is released it should turn on
if LED was on it should turn off
two flip flops
    1) remember the state of the LED
    2) detect when switch is released

we're going to look for falling edge

*/

module LED_Toggle
(
    input i_Clk,
    input i_Switch_1,
    output o_LED_1
);
    reg r_Switch_1 = 1'b0;
    reg r_LED_1 = 1'b0;

    always @(posedge i_Clk)begin
        r_Switch_1 <= i_Switch_1;
        if (i_Switch_1 == 1'b0 && r_Switch_1 == 1'b1) begin
            r_LED_1 = ~r_LED_1;
        end 
    end


    assign o_LED_1 = r_LED_1;

endmodule



