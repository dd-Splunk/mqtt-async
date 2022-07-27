#!/bin/bash
source .env
# Bring up the environment
docker compose up -d

echo -e "\nWait for login prompt"
until $(curl -s -f -o /dev/null -k --head "http://$SPLUNK_HOST:8000")
do
  echo -n '.'
  sleep 10
done
