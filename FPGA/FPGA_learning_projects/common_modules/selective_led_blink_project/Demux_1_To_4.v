module Demux_1_4(
    input i_data,
    input i_select_0,
    input i_select_1,
    output o_data_0,
    output o_data_1,
    output o_data_2,
    output o_data_3
);
    assign o_data_0 = (i_select_0 & i_select_1) ? i_data : 1'b0;
    assign o_data_1 = (!i_select_0 & i_select_1) ? i_data : 1'b0;
    assign o_data_2 = (i_select_0 & !i_select_1) ? i_data : 1'b0;
    assign o_data_3 = (!i_select_0 & !i_select_1) ? i_data : 1'b0;
    
endmodule