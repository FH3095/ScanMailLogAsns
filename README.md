# What is this for?
This is my personal block-file for postfix to block auth-attempts from some ASNs because I observed these ASNs in many auth-tries with different IP addresses.
I use this in my postfix-conf: `smtpd_discard_ehlo_keyword_address_maps = cidr:/etc/postfix/blockedAsns.cidr`
The mapping from ASN to IP-Blocks is provided by https://github.com/ipverse/asn-ip

# How to use it
There are two ways to use it: Either create your own blockedAsns.json, enter ASNs there and run updateAll.sh. You should run updateAll.sh regularly in order to update the IP-Addresses for the blocked ASNs.
Or you regularly pull from this repository and copy the blockedAsns.cidr.example to `/etc/postfix`. I keep this file up-to-date with my personal blockedAsns.cidr.
