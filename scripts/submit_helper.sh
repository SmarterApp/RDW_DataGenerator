#!/usr/bin/env bash
# This script is invoked by submit_driver.sh to process a sub-folder
# $1 - sub-folder, usually the school folder

s=$1

HOST="http://localhost:8080"
#HOST="https://awsuat-import.sbacdw.org"

# fetch bearer token (need jq installed)
#ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=username&password=password&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token'`
# if host is using the "stub" token service, use this instead:
ACCESS_TOKEN="sbac;dwtest@example.com;|SBAC|ASMTDATALOAD|CLIENT|SBAC||||||||||||||"

echo "processing ${s} using access token ${ACCESS_TOKEN}"
for xml in ${s}/*.xml; do
    echo "submitting $xml"
    curl -X POST --header "Authorization:Bearer ${ACCESS_TOKEN}" -F file=@"${xml}" ${HOST}/exams/imports
done
