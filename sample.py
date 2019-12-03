#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ipaddress
import json
import urllib.request

if __name__ == "__main__":

    ip = ipaddress.ip_address('13.64.0.1')

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

    #print(body)
    json_dict = json.loads(body)
    #print('json_dict:{}'.format(json_dict))
    msg = ''

    for region in json_dict :
        #print( '--------------------------------------' )
        #print(str(region))
        #print( '--------------------------------------' )

        if json_dict[region] is not None:
            for network in json_dict[region]:
                #print(str(network))
                nw = ipaddress.ip_network(network)

                for addr in nw:
                    if addr == ip:
                        msg = str(ip) + " in " + str(region) + ":" + str(nw)
                        print(msg)
                        break
            
            if msg is not None: break
        if msg is not None: break

