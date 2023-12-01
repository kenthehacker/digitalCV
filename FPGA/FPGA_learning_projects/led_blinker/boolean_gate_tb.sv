// Code your testbench here
// or browse Examples
module And_gate_tb();
    reg r_Switch_1, r_Switch_2;
    wire w_Out;
    and_gate_led UUT(
        .i_Switch_1(r_Switch_1),
        .i_Switch_2(r_Switch_2),
        .o_LED_1(w_Out)
    );
    initial begin
        $dumpfile("dump.vcd"); $dumpvars;
        r_Switch_1 <= 1'b0;
        r_Switch_2 <= 1'b0;
        #10;

        r_Switch_1 <= 1'b1;
        r_Switch_2 <= 1'b0;
        #10;

        r_Switch_1 <= 1'b0;
        r_Switch_2 <= 1'b1;
        #10;

        r_Switch_1 <= 1'b1;
        r_Switch_2 <= 1'b1;
        #10

      $finish;
    end

endmodule