### Led Selection table
i_Switch_2  i_Switch_1  Which LED?
~~~
0      |    0    |      1
0      |    1    |      2
1      |    0    |      3
1      |    1    |      4
~~~
### Timing
Clock runs at 25 MHz we want LED to blink at 2HZ
25MHz = 25,000,000 clock cycles per second. We can count clock cycle or use LFSR to delay 
N flip flop LSR will take 2^N - 1 clock cycle for pattern to cycle through

We want 2HZ or 25% of one second since there's on-off cycles two times per second 
25,000,000 * (0.25) = 6,250,000 clock cycles needed
log_2(6,250,000 + 1) = 22.5754249899 = N
Let's round up to use N = 23


### Design
LFSR -> D-Flip Flop -> 
             Switch ->
                        1-4 Demux -> LED Output
