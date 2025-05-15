#!/bin/bash

# Define the Python scripts to run in the order
commands=(
  "python run.py mars --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method random1 --seed 46"
  "python run.py mars --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method best100"
  "python run.py mars --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method worst100"
)

# Print and execute each command
for cmd in "${commands[@]}"; do
  echo "Executing: $cmd"   # Print the command
  $cmd                    # Execute the command
done
