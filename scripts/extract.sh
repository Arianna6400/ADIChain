#!/bin/bash
echo "Starting Docker Compose services..."
docker-compose up -d

echo "Wait 10 seconds for Ganache to start..."
sleep 10

echo "Extracting Ganache's log..."
docker-compose logs --tail=80 ganache | grep -A 50 "Available Accounts\|Private Keys" > accounts.txt

echo "All the local information for registration purpose are extracted in accounts.txt"
