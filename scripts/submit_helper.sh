#!/usr/bin/env bash
# This script is invoked to process a sub-folder of TRT files.
# $1 - sub-folder, usually the school folder
#
# To process a bunch of folders use this in conjunction with find and xargs. This
# example launches up to 8 processes to submit all the school folder contents:
# find ./out/*/*/* -type d | xargs -I FOLDER -P 8 ./scripts/submit_helper.sh FOLDER

s=$1

HOST="http://localhost:8080"
#HOST="http://awsqa-import.sbacdw.org"
#HOST="https://awsuat-import.sbacdw.org"

# fetch bearer token (need jq installed)
#ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=mlaffoon@fairwaytech.com&password=mlaffoon&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token'`
#ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=dwtest@example.com&password=password&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token'`
# if host is using the "stub" token service, use this instead:
ACCESS_TOKEN="sbac;dwtest@example.com;|SBAC|ASMTDATALOAD|CLIENT|SBAC||||||||||||||"

echo "processing ${s} using access token ${ACCESS_TOKEN}"
for xml in ${s}/*; do
#    echo "submitting $xml"
    curl -X POST -s --header "Authorization:Bearer ${ACCESS_TOKEN}" -F file=@"${xml}" ${HOST}/exams/imports | jq -c --arg FN "${xml}" '. | {file: $FN, id: .id, status: .status}'
done
