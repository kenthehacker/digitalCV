// Code your testbench here
// or browse Examples
module Turnstile_tb();
    reg r_Reset = 1'b1;
    reg r_Clk = 1'b0;
    reg r_Coin = 1'b0;
    reg r_Push = 1'b0;
    wire w_Locked;
    localparam LOCKED = 1'b1;
    localparam UNLOCKED = 1'b0;

    Turnstile_oneblock UUT(
        .i_Reset(r_Reset),
        .i_Clk(r_Clk),
        .i_Coin(r_Coin),
        .i_Push(r_Push),
        .o_locked(w_Locked)//we know its a wire because in Turnstile_oneblock.v we use 'assign'
    );

    always #1 r_Clk<=!r_Clk; // period is two units 50% up time

    initial begin
        $dumpfile("turnstile_1b_dump.vcd");
        $dumpvars;
        r_Reset <= 1'b1;
        #10; // Wait for 10 time units
        if (w_Locked === LOCKED)
            $display("Test 1: PASSED");
        else
            $display("Test 1: FAILED");
        r_Reset<=1'b0;
        r_Coin <= 1'b1;
        #10;
        if (w_Locked === UNLOCKED)
            $display("Test 2: PASSED");
        else
            $display("Test 2: FAILED");

        r_Push <= 1'b1;
        #10;
        if (w_Locked === LOCKED)
            $display("Test 3: PASSED");
        else
            $display("Test 3: FAILED");

        r_Coin <= 1'b0;
        #10;
        if (w_Locked === LOCKED)
            $display("Test 4: PASSED");
        else
            $display("Test 4: FAILED");

        $finish; // End simulation
    end



endmodule