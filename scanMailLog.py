#!/usr/bin/env python3

import sys, os, json, re, gzip, ipaddress

FIND_REGEX = re.compile(r'\[([0-9.]+)\]: (?:(?:SASL LOGIN authentication failed))', re.I)
#FIND_REGEX = re.compile(r'\[([0-9.]+)\] blocked using zen.spamhaus.org', re.I)

def openFile(file):
	if file.endswith(".gz"):
		return gzip.open(file, 'rt', encoding='utf-8')
	else:
		return open(file, 'rt', encoding='utf-8')

def readFile(ipAddresses, file):
	with openFile(file) as f:
		for line in f:
			match = FIND_REGEX.search(line)
			if match != None:
				ipAddresses[match.group(1)] = ipAddresses.get(match.group(1), 0) + 1

def readAllFiles(argv):
	ipAddresses = {}
	for file in argv:
		readFile(ipAddresses, file)
	return ipAddresses

def readJson(filePath):
	with gzip.open(filePath, mode='rt', encoding='utf-8') as file:
		return json.load(file)

def findAsn(ips, ip):
	net = ipaddress.IPv4Network(ip)
	while net.prefixlen > 0:
		if net.with_prefixlen in ips:
			return ips[net.with_prefixlen]
		net = net.supernet()
	return []

def printAsn(asn, asns):
	asnStr = str(asn[0])
	msg = str(asn[1]) + ' matches: ' + asnStr
	if asnStr in asns:
		asnInfo = asns[asnStr]
		msg = msg + ' ('
		if 'name' in asnInfo:
			msg = msg + asnInfo['name']
		else:
			msg = msg + '?'
		msg = msg + ' '
		if 'desc' in asnInfo:
			msg = msg + asnInfo['desc']
		msg = msg + ')'
	print(msg)

asns = readJson('asns.json.gz')
ips = readJson('ips.json.gz') 
foundIps = readAllFiles(sys.argv[1:])

foundPerAsn = {}

for ip, num in foundIps.items():
	for asn in findAsn(ips, ip):
		foundPerAsn[asn] = foundPerAsn.get(asn, 0) + num
foundPerAsn = sorted(foundPerAsn.items(), key=lambda item: item[1])
for asn in foundPerAsn:
	printAsn(asn, asns)
