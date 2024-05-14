#!/bin/bash

# Avvia tutti i servizi definiti nel file docker-compose.yml
docker-compose up -d


# Ottiene l'ID del container per il servizio adichain
ADI_CHAIN_CONTAINER_ID=$(docker-compose ps -q adichain)

# Controlla se l'ID del container è stato trovato
if [ -z "$ADI_CHAIN_CONTAINER_ID" ]; then
    echo "Il container adichain non è stato trovato. Assicurati che il servizio sia definito correttamente nel tuo docker-compose.yml."
    exit 1
fi

echo "Attaching to adichain container ($ADI_CHAIN_CONTAINER_ID)..."
# Si attacca al container adichain
winpty docker attach "$ADI_CHAIN_CONTAINER_ID"

docker wait "$ADI_CHAIN_CONTAINER_ID"

docker-compose stop
