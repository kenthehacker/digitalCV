#!/bin/bash

# Define the C program executable
program="./client"

# Loop 5 times and run the C program each time
for i in {1..5}
do
    # Run the C program in the background
    $program 128.252.167.161 30303&
done

# Wait for all background processes to complete
wait
