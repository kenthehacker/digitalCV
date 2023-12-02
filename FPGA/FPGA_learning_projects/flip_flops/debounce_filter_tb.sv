module Debounce_Filter_Tb();
    reg r_Switch_1 = 1'b0;
    reg r_Clk = 1'b0;
    
    //invert clock signal every 2ns => 50% duty cycle for clock cycle time of 4ns
    //works since its just a test code; real board uses 25mhz
    always #2 r_Clk <= ~r_Clk;
    wire w_Debounced;

    Debounce_Filter #(.DEBOUNCE_LIMIT(4)) UUUT(
        .i_Clk(r_Clk),
        .i_Switch_1(r_Switch_1),
        .o_Debounced(w_Debounced)
    );

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars;
        repeat(4) @(posedge r_Clk);             //enables code to start off right
        r_Switch_1 <= 1'b1;

        @(posedge r_Clk);                       //wait for a clock cycle before assignment
        r_Switch_1 <= 1'b0;

        @(posedge r_Clk);
        r_Switch_1 <= 1'b1;

        repeat(10) @(posedge r_Clk);            //gives debouncer more time to process clock changes
        $display("Testbench simulation completed.");
        $finish();

    end 


endmodule


// = is a blocking assignment <= is a non blocking assignment 