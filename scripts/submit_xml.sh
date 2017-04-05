#!/usr/bin/env bash
#
# Script to post XML files.
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CREDS="-u dwtest@example.com:password"
HOST="http://localhost:8080"

pushd "$SCRIPT_DIR/../out"

for xml in *.xml; do
    echo "submitting $xml"
    curl -X POST ${CREDS} --header "Content-Type:application/xml" --data-binary @${xml} ${HOST}/exams/imports
done

popd
