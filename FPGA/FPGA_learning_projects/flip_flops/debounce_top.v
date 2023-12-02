/*
physical switch -> [ Debounce Top Module (this file)
    -> [Debounce Switch module] -> debounced output
    -> [led_toggle module]
    -> physical LED
]

cycle duration = 1/freq
1/25mhz = 1/25,000,000 hz
1s = 1,000,000,000ns
1s * (1/25 mhz) = 40ns (cycle duration = 40ns)
10ms/40ns = 10,000,000/40 = 250,000 cycles to get 10ms
*/

module Debounce_Top(
    input i_Switch_1,
    input i_Clk,
    output o_LED_1
);
    wire w_debounced_switch;
    Debounce_Filter #(.DEBOUNCE_LIMIT(250000)) filter_inst (
        .i_Clk(i_Clk),
        .i_Switch_1(i_Switch_1),
        .o_Debounced(w_debounced_switch)
    );

    LED_Toggle led_toggle_inst (
        .i_Switch_1(w_debounced_switch),
        .i_Clk(i_Clk),
        .o_LED_1(o_LED_1)
    );


endmodule