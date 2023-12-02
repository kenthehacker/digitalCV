module Debounce_Filter
(
    input i_Switch_1,
    input i_Clk,
    output o_Debounced
);
    parameter DEBOUNCE_LIMIT = 256;
    reg [$clog2(DEBOUNCE_LIMIT) -1 : 0] r_cycle_count = 0;
    reg r_button_state = 1'b0;
    always @(posedge i_Clk)begin 
        if (r_cycle_count<DEBOUNCE_LIMIT-1 && r_button_state !== i_Switch_1) begin
            r_cycle_count <= r_cycle_count + 1;
        end else if(r_cycle_count == DEBOUNCE_LIMIT-1) begin
            r_cycle_count <= 0;
            r_button_state <= i_Switch_1;
        end else begin
            r_cycle_count <= 0;
        end
    end 
    assign o_Debounced = r_button_state;

endmodule