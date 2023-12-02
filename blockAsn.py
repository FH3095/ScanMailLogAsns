#!/usr/bin/env python3

import sys, os, json, gzip

REJECT_MSG = 'REJECT ASN {0} is blocked due to repeated password guesses'

def getCidrLinesForAsn(asn):
	result = '# ASN ' + str(asn) + '\n'
	filePath = 'asn-ip/as/' + str(asn) + '/aggregated.json'
	if os.path.isfile(filePath):
		with open(filePath, mode='rt') as f:
			data = json.load(f)
			if 'subnets' in data and 'ipv4' in data['subnets']:
				for ip4 in data['subnets']['ipv4']:
					result = result + ip4 + '\t' + REJECT_MSG.format(str(asn)) + '\n'
	result = result + '\n'
	return result

blockedAsns = []
with open('blockedAsns.json', mode='rt') as f:
	blockedAsns = json.load(f)

with open('blockedAsns.cidr', mode='wt') as f:
	for asn in blockedAsns:
		f.write(getCidrLinesForAsn(asn))
