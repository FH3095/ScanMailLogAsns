#!/bin/sh

echo "### UPDATE"
git pull

echo "### UPDATE ASN-IPs"
if [ ! -d "asn-ip" ]; then
	git clone https://github.com/ipverse/asn-ip.git asn-ip
fi
cd asn-ip
git pull
cd ..

echo "### UPDATE CIDR"
./convertAsn.py
./blockAsn.py
cp blockedAsns.cidr /etc/postfix/blockedAsns.cidr
