#!/bin/sh

oldcwd="$(pwd)"
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

./updateAll.sh

cp blockedAsns.json blockedAsns.json.example
cp blockedAsns.cidr blockedAsns.cidr.example
today="$(date --utc --iso-8601=date)"
git commit -m "Regular update $today" blockedAsns.json.example blockedAsns.cidr.example
git push
