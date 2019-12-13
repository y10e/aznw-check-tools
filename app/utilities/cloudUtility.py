import ipaddress
import json
import urllib.request
import sys
import subprocess
import re
import dns.resolver

global gcpip4
gcpip4 = set()

def CheckIP(ipaddr):
    ip = ipaddress.ip_address(ipaddr)
    msg = str(ipaddr) + "\n"

    CheckAzureResult = CheckAzureIPs(ipaddr)
    msg += CheckAzureResult
    if CheckAzureResult == "" :
        CheckAWSResult = CheckAWSIPs(ipaddr)
        msg += CheckAWSResult
        if CheckAWSResult == "" :
            CheckGCPResult = CheckGCPIPs(ipaddr)
            msg += CheckGCPResult
            if CheckGCPResult == "":
                CheckGithubResult = CheckGithubIPs(ipaddr)
                msg += CheckGithubResult
                if CheckGithubResult == "":
                    msg += str(ipaddr) + " does not contain Azure/AWS/GCP/Github Public IP Addresses." + "\n"

    msg += "$" + "\n"
    res = subprocess.run(["whois",str(ipaddr)], stdout=subprocess.PIPE)
    msg += "$ whois " + str(ipaddr) + "\n" + res.stdout.decode('utf-8') + "\n"
    return msg

def CheckAzureIPs(ipaddr):
    ip = ipaddress.ip_address(ipaddr)
    msg = ""

    url = 'https://azuredcip.azurewebsites.net/api/azuredcipranges'
    data = {
        'region': 'all',
        'request':'dcip',
    }
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)

    with urllib.request.urlopen(req) as res:
        body = res.read()

    json_dict = json.loads(body)
    IsResult = False

    for region in json_dict :
        if json_dict[region] is not None:
            #print(region)
            for network in json_dict[region]:
                #print(str(network))
                nw = ipaddress.ip_network(network)

                for addr in nw:
                    if addr == ip:
                        msg += str(ip) + " belongs to " + str(nw) + " in Azure " + str(region).upper() + "." + "\n"
                        IsResult = True
                        break
            
            if IsResult: break
        if IsResult: break

    return msg

def CheckAWSIPs(ipaddr):

    ip = ipaddress.ip_address(ipaddr)
    msg = ""

    url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(req) as res:
        body = res.read()

    json_dict = json.loads(body)
    IsResult = False

    for prefix in json_dict["prefixes"] :
        print(prefix)
        if str(prefix["service"]).upper() == "AMAZON" : continue
        nw = ipaddress.ip_network(prefix["ip_prefix"])
        for addr in nw:
            if addr == ip:
                msg += str(ip) + " belongs to " + str(nw) + " in AWS " + str(prefix["region"]).upper() + " (" + str(prefix["service"]).upper() +  ")." + "\n"
                IsResult = True
                break
        if IsResult: break
    return msg

def CheckGCPIPs(ipaddr):
    spf_gcp = '_cloud-netblocks.googleusercontent.com'
    search_dns(spf_gcp)
    print(gcpip4)
    ip = ipaddress.ip_address(ipaddr)
    msg = ""

    IsResult = False
    for prefix in gcpip4 :
        nw = ipaddress.ip_network(prefix)
        for addr in nw:
            if addr == ip:
                msg += str(ip) + " belongs to " + str(nw) + " in Google Cloud Platform" +  "." + "\n"
                IsResult = True
                break
        if IsResult: break

    return msg 

def search_dns(target):
    global gcpip4
    for dns_info in dns.resolver.query(target, 'TXT'):
        servers = re.findall(r'include:(\S*)', str(dns_info))
        if len(servers) > 0:
            for s in servers:
                print(f'searching domain: {s}')
                search_dns(s)
        gcpip4 |= set(re.findall(r'ip4:(\S*)', str(dns_info)))

def CheckGithubIPs(ipaddr):
    ip = ipaddress.ip_address(ipaddr)
    msg = ""

    url = 'https://api.github.com/meta'
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(req) as res:
        body = res.read()

    json_dict = json.loads(body)
    IsResult = False
    list = ["hooks","web","api","git","pages","importer"]

    for item in json_dict :
        if item in list :
            for network in json_dict[item]:
                nw = ipaddress.ip_network(network)

                for addr in nw:
                    if addr == ip:
                        msg += str(ip) + " belongs to " + str(nw) + " in Github " + str(item).upper() + " Service." + "\n"
                        IsResult = True
                        break

            if IsResult: break
        if IsResult: break

    return msg
    