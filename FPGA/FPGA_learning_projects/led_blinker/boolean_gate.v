/*
Learned about LUTs and boolean logic so just wanted to try it out here
LED1 will turn on if both switch 1 and switch 2 are pressed on the board 
*/
module and_gate_led(
    input i_Switch_1,
    input i_Switch_2,
    output o_LED_1
);
    assign o_LED_1 = i_Switch_1 & i_Switch_2;
endmodule
