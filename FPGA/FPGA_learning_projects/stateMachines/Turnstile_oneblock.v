//samething but uses one block method
module Turnstile_oneblock(
    input i_Reset,
    input i_Clk,
    input i_Coin,
    input i_Push,
    output o_locked
);
    localparam LOCKED = 1'b1;
    localparam UNLOCKED = 1'b0;
    reg r_Curr_State;
    always @(posedge i_Clk or posedge i_Reset) begin
        if (i_Reset)
            r_Curr_State <= LOCKED;
        else begin
            case (r_Curr_State)
                LOCKED:
                    if (i_Coin)
                        r_Curr_State <= UNLOCKED;
                UNLOCKED:
                    if (i_Push)
                        r_Curr_State <= LOCKED;
            endcase
        end 
    end 
    assign o_locked = (r_Curr_State == LOCKED);
endmodule
