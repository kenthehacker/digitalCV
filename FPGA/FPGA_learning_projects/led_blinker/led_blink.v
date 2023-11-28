module led_blink (
    i_clock,
    i_enable,
    i_Switch_1,
    i_Switch_2,
    o_led_power
);
    input i_clock;
    input i_enable;
    input i_Switch_1;
    input i_Switch_2;
    output o_led_power;

    // Clock cycles for different frequency at 50% duty
    parameter p_clock_cycle_100 = 125 - 1;
    parameter p_clock_cycle_50 = 250 - 1;
    parameter p_clock_cycle_10 = 1250 - 1;
    parameter p_clock_cycle_1 = 12500 - 1;

    reg [31:0] r_cycle_count_100 = 0;
    reg [31:0] r_cycle_count_50 = 0;
    reg [31:0] r_cycle_count_10 = 0;
    reg [31:0] r_cycle_count_1 = 0;

    reg r_signal_100 = 1'b0;
    reg r_signal_50 = 1'b0;
    reg r_signal_10 = 1'b0;
    reg r_signal_1 = 1'b0;

    reg r_led_mode;

    // Always block for 100 Hz
    always @ (posedge i_clock) begin
        if (r_cycle_count_100 >= p_clock_cycle_100) begin
            r_cycle_count_100 <= 0;
            r_signal_100 <= !r_signal_100;
        end else begin
            r_cycle_count_100 <= r_cycle_count_100 + 1;
        end
    end

    // Always block for 50 Hz
    always @ (posedge i_clock) begin
        if (r_cycle_count_50 >= p_clock_cycle_50) begin
            r_cycle_count_50 <= 0;
            r_signal_50 <= !r_signal_50;
        end else begin
            r_cycle_count_50 <= r_cycle_count_50 + 1;
        end
    end

    // Always block for 10 Hz
    always @ (posedge i_clock) begin
        if (r_cycle_count_10 >= p_clock_cycle_10) begin
            r_cycle_count_10 <= 0;
            r_signal_10 <= !r_signal_10;
        end else begin
            r_cycle_count_10 <= r_cycle_count_10 + 1;
        end
    end

    // Always block for 1 Hz
    always @ (posedge i_clock) begin
        if (r_cycle_count_1 >= p_clock_cycle_1) begin
            r_cycle_count_1 <= 0;
            r_signal_1 <= !r_signal_1;
        end else begin
            r_cycle_count_1 <= r_cycle_count_1 + 1;
        end
    end

    always @ (*) begin
        if ({i_Switch_1, i_Switch_2} == 2'b00) begin
            r_led_mode <= r_signal_100;
        end else if ({i_Switch_1, i_Switch_2} == 2'b01) begin
            r_led_mode <= r_signal_50;
        end else if ({i_Switch_1, i_Switch_2} == 2'b10) begin
            r_led_mode <= r_signal_10;
        end else if ({i_Switch_1, i_Switch_2} == 2'b11) begin
            r_led_mode <= r_signal_1;
        end
    end
    assign o_LED_1 = r_led_mode & i_enable;
endmodule
