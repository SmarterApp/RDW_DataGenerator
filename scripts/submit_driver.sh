#!/usr/bin/env bash
# This scripts spawns multiple processes to more quickly submit xml files.
# It should be run from the parent folder of 'out'.
#
# To submit all schools in a district folder, move to the district folder and replace outer loop:
# for s in *; do

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# files are grouped by STATE/DISTRICT/SCHOOL
for s in ./out/CA/*/*; do
  echo "partitioning $s"
  for p in 0 1 2 3 4 5 6 7 8 9 a b c d e f ; do
    ${SCRIPT_DIR}/submit_helper.sh ${s} ${p} &
  done
  wait
done
