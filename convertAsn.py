#!/usr/bin/env python3

import sys, os, json, gzip

def readAsnIps(data, asn, ips):
	if 'prefixes' in data and 'ipv4' in data['prefixes']:
		for ip4Str in data['prefixes']['ipv4']:
			ip4 = ip4Str.strip()
			if not ip4 in ips:
				ips[ip4] = []
			ips[ip4].append(asn)

def readAsnName(data, asn, asns):
	asns[asn] = {}
	if 'metadata' in data:
		metadata = data['metadata']
		if 'handle' in metadata:
			asns[asn]['name'] = metadata['handle']
		if 'description' in metadata:
			asns[asn]['desc'] = metadata['description']

def readAsns(asnPath):
	asns = {}
	ips = {}
	cnt = 0
	for dir in os.scandir(asnPath):
		if dir.is_dir():
			cnt = cnt + 1
			if cnt % 10000 == 0:
				print('Scanned ' + str(cnt) + ' asns')
			filePath = os.path.join(dir.path, 'aggregated.json')
			if os.path.isfile(filePath):
				with open(filePath, 'rt') as f:
					data = json.load(f)
					readAsnName(data, int(dir.name), asns)
					readAsnIps(data, int(dir.name), ips)
	return ips, asns

def writeFile(filePath, ips):
	with gzip.open(filePath, mode='wt', encoding='utf-8') as file:
		json.dump(ips, file)

ips, asns = readAsns('asn-ip/as/')
writeFile('ips.json.gz', ips)
writeFile('asns.json.gz', asns)
