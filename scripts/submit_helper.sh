#!/usr/bin/env bash
# This script is invoked by submit_driver.sh to process a subset of files in a sub-folder.
# $1 - sub-folder, usually the school folder
# $2 - prefix of files to process, e.g. '4'

s=$1
p=$2

HOST="http://localhost:8080"

# fetch bearer token (need jq installed)
#ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=dwtest@example.com&password=password&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token'`
# if host is using the "stub" token service, use this instead:
ACCESS_TOKEN="sbac;dwtest@example.com;|SBAC|ASMTDATALOAD|CLIENT|SBAC||||||||||||||"

for xml in ${s}/${p}*.xml; do
    echo "submitting $xml"
    curl -X POST --header "Authorization:Bearer ${ACCESS_TOKEN}" -F file=@"${xml}" ${HOST}/exams/imports
done
