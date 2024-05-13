#!/bin/bash
output_file="passwords.txt"

> "$output_file"

generate_password() {
    while true; do
        password=$(openssl rand -base64 32 | tr -dc 'A-Za-z0-9@#$%^&+=' | fold -w 16 | head -n 1)
        if echo "$password" | python -c "import sys, re; print('True' if re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?!.*\s).{8,100}$', sys.stdin.read().strip()) else 'False')" | grep -q "True"; then
            echo $password
            break
        fi
    done
}

for i in $(seq 1 10); do
    generate_password >> "$output_file"
done

echo "Passwords generated and saved in '$output_file'."
