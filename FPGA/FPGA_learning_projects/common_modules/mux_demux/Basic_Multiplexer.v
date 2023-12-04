/*
4 input 1 output
2 select 

0 0: data_0
0 1: data_1
1 0: data_2
1 1: data_3
*/

module Basic_Multiplexer
(
input i_select_0,
input i_select_1,
input i_data_0,
input i_data_1,
input i_data_2,
input i_data_3,
output o_data
);
    assign o_data = (!i_select_0 && !i_select_1)? i_data_0 : 
                    (!i_select_0 && i_select_1) ? i_data_1 :
                    (i_select_0 && !i_select_1) ? i_data_2 : i_data_3;
    //above is nested ternary operator


endmodule












