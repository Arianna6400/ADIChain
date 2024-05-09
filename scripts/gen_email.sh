#!/bin/bash
num_emails=10
domain="adichain.com"

output_file="emails.txt"
> "$output_file"

for ((i=1; i<=num_emails; i++))
do
  username=$(tr -dc 'a-z' </dev/urandom | head -c $(($RANDOM % 6 + 5)))
  email="$username@$domain"
  echo $email >> "$output_file"
done

echo "Emails saved to $output_file"
