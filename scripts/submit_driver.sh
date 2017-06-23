#!/usr/bin/env bash
# This scripts spawns multiple processes to more quickly submit xml files.
# It is expecting to run for a single district, spawning processes for the schools one-at-a-time.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

for s in *; do
  echo "partitioning $s"
  for p in 0 1 2 3 4 5 6 7 8 9 a b c d e f ; do
    ${SCRIPT_DIR}/submit_helper.sh $s $p &
  done
  wait
done
