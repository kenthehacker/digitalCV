/*
Basic turnstile state machine via two-block FSM
Turnstile is a simple device which gives you an access if payment is made 
and is a very simple to model using a state machine. In its simplest form there are 
only two states, LOCKED and UNLOCKED . Two events, COIN and PUSH can happen 
if you try to go through it or you make a payment.

the reason why we make two blocks is because synthesizers before werent that good
and made mistakes. this two block method was a get around and is now just 
the way a lot of programmers do it now
*/

module Turnstile(
    input i_Reset,
    input i_Clk,
    input i_Coin,
    input i_Push,
    output o_locked
);
    localparam LOCKED = 1'b1;
    localparam UNLOCKED = 1'b0;
    reg r_Curr_State;
    reg r_Next_State;

    //next state logic
    always @(r_Curr_State or posedge i_Coin or posedge i_Push)begin
        r_Next_State <= r_Curr_State;
        case(r_Curr_State)
            LOCKED:
                if (i_Coin)
                    r_Next_State<=UNLOCKED;
            UNLOCKED:
                if (i_Push)
                    r_Next_State<=LOCKED;
        endcase
    end 

    //current state logic
    always @(posedge i_Reset or posedge i_Clk)begin
        if (i_Reset)
            r_Curr_State = LOCKED;
        else
            r_Curr_State <= r_Next_State;
    end 
    assign o_locked = (r_Curr_State==LOCKED);

endmodule
