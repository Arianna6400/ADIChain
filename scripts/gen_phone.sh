#!/bin/bash

num_numeri=10
output_file="phone_numbers.txt"

prefissi_mobili=("320" "330" "340" "350" "360" "370" "380" "390")
prefissi_fissi=("02" "06" "011" "015" "081" "091" "049" "041")

> "$output_file"

for ((i=1; i<=num_numeri; i++))
do
  if (( RANDOM % 2 )); then
    prefisso="${prefissi_mobili[$RANDOM % ${#prefissi_mobili[@]}]}"
  else
    prefisso="${prefissi_fissi[$RANDOM % ${#prefissi_fissi[@]}]}"
  fi

  numero=$(shuf -i 1000000-9999999 -n 1)

  numero_telefonico="$prefisso$numero"

  echo $numero_telefonico >> "$output_file"
done

echo "Phone numbers saved in $output_file"
