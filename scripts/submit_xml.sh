#!/usr/bin/env bash
#
# Script to post XML files.
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "$SCRIPT_DIR/../out"

HOST="http://localhost:8080"
#HOST="https://awsqa-import.sbacdw.org"
#HOST="https://awsuat-import.sbacdw.org"

# files are grouped by STATE/DISTRICT/SCHOOL
COUNT=1000000
for xml in */*/*/*.xml; do
    if [ ${COUNT} -gt 10000 ]; then
        # fetch bearer token (need jq installed)
#        ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=dwtest@example.com&password=password&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token' `
#        ACCESS_TOKEN=`curl -s -X POST --data 'grant_type=password&username=mlaffoon@fairwaytech.com&password=mlaffoon&client_id=sbacdw&client_secret=sbacdw123' 'https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac' | jq -r '.access_token' `
        # if host is using the "stub" token service, use this instead:
        ACCESS_TOKEN="sbac;dwtest@example.com;|SBAC|ASMTDATALOAD|CLIENT|SBAC||||||||||||||"
        echo "reset access token: ${ACCESS_TOKEN}"
        COUNT=0
    fi

#    echo "submitting $xml"
    curl -X POST -s --header "Authorization:Bearer ${ACCESS_TOKEN}" -F file=@"${xml}" ${HOST}/exams/imports | jq -c --arg FN "${xml}" '. | {file: $FN, id: .id, status: .status}'
    COUNT=$((COUNT + 1))
done

popd
