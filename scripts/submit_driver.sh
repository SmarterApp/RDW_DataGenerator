#!/usr/bin/env bash
# This scripts spawns multiple processes to more quickly submit xml files.
# It should be run from the parent folder of 'out'.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# files are grouped by ./out/STATE/DISTRICT/SCHOOL
# one DISTRICT at a time, each SCHOOL folder is given to a submit helper
for d in ./out/*/*; do
  echo "partitioning $d"
  for f in ${d}/*; do
    ${SCRIPT_DIR}/submit_helper.sh ${f} &
  done
  wait
done
