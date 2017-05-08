#!/usr/bin/env bash
#
# Script to post XML files.
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "$SCRIPT_DIR/../out"

# fetch bearer token (need jq installed)
HOST="http://localhost:8080"
ACCESS_TOKEN=`curl -s -X POST --data "grant_type=password&username=dwtest@example.com&password=password&client_id=ets&client_secret=ets123" https://sso-deployment.sbtds.org:443/auth/oauth2/access_token?realm=/sbac | jq -r '.access_token'`

# files are grouped by STATE/DISTRICT/SCHOOL
for xml in */*/*/*.xml; do
    echo "submitting $xml"
    curl -X POST --header "Authorization:Bearer ${ACCESS_TOKEN}" --header "Content-Type:application/xml" --data-binary @"${xml}" ${HOST}/exams/imports
done

popd
