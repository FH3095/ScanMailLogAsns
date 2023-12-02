#!/bin/sh

git pull
git submodule update --remote --rebase
./convertAsn.py
./blockAsn.py
cp blockedAsns.cidr /etc/postfix/blockedAsns.cidr
