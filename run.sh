#!/bin/bash

# Define the Python scripts to run in the order
commands=(
  #"python run.py gpbo --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method best100"
  "python run.py gpbo --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method worst100"
  "python run.py jt_vae --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method best100"
  "python run.py jt_vae --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method worst100"
  "python run.py graph_ga --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method best100"
  "python run.py graph_ga --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1 --init_method worst100"
)

# Print and execute each command
for cmd in "${commands[@]}"; do
  echo "Executing: $cmd"   # Print the command
  $cmd                    # Execute the command
done
