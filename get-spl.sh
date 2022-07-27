#!/bin/bash
APP=${PWD##*/}
APP_FILE=${APP}.spl
APP_LOCATION=/opt/splunk/share/splunk/app_packages/${APP_FILE}
source .env
echo "Asking Splunk to package ${APP_FILE} ..."
curl -s -k -u admin:$SPLUNK_PASSWORD https://$SPLUNK_HOST:8089/services/apps/local/$APP/package
echo "Downloading ${APP_FILE} ..."
docker cp so1:$APP_LOCATION .
echo "Expanding ${APP_FILE} ..."
tar  -C app/ -xf ${APP_FILE} --strip 1
# Remove lookup editor backups
rm -rf app/lookups/lookup_file_backups
rm ${APP_FILE}
echo "Done."
#
