#!/bin/bash
source .env
# Bring up the environment
docker compose up -d

# echo "Wait for Splunk availability"

# REGEX="<sessionKey>(.+)<\/sessionKey>"
# until [[ "$(curl -k -s -u admin:$SPLUNK_PASSWORD https://$SPLUNK_HOST:8089/services/auth/login -d username=admin -d password=$SPLUNK_PASSWORD)" =~ $REGEX ]]; do
#   echo -n '.'
#   sleep 10
# done
# # https://stackoverflow.com/questions/1891797/capturing-groups-from-a-grep-regex
# sessionKey=${BASH_REMATCH[1]}

echo -e "\nChange App $SPLUNK_APP permission to Global"
until $(curl -s -f -o /dev/null -k -u admin:$SPLUNK_PASSWORD --request POST "https://$SPLUNK_HOST:8089/services/apps/local/$SPLUNK_APP/acl" -d sharing=global -d owner=nobody)
do
  echo -n '.'
  sleep 10
done
#
echo -e "\nEnable EventGen"
until $(curl -s -f -o /dev/null -k -u admin:$SPLUNK_PASSWORD --request POST "https://$SPLUNK_HOST:8089/servicesNS/nobody/SA-Eventgen/data/inputs/modinput_eventgen/default/enable")
do
  echo -n '.'
  sleep 10
done
#
echo -e "\nWait for login prompt"
until $(curl -s -f -o /dev/null -k --head "http://$SPLUNK_HOST:8000")
do
  echo -n '.'
  sleep 10
done
