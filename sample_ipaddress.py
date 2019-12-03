#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ipaddress

if __name__ == "__main__":

    ip = ipaddress.ip_address('10.2.3.4')
    nw = ipaddress.ip_network('10.0.0.0/8')

    if ip in nw: # ip in network の1行でネットワークアドレスに含まれるか判別が可能
        print ("%s is included %s ."%(ip, nw))
    else :
        print ("%s isn't included %s ."%(ip, nw))

    print ("="*15)

    ip = ipaddress.ip_address('10.2.3.255')
    ipv6 = ipaddress.ip_address('fd00:260:301:104::104:1')
    ex_ipv6 = ipaddress.ip_address('fd00:0260:0301:0104:0000:0000:0104:1')

    #ipv4/v6どちらのアドレスが格納されているか確認
    print ("%s  is IPv%d"%(ip,ip.version))
    print ("%s  is IPv%d"%(ipv6,ipv6.version))
    print ("="*15)
    
    #アドレスのインクリメント
    ip = ip + 1
    ipv6 = ipv6 -2
    print ("increment ipv4 : %s"%ip)
    print ("decrement ipv6 : %s"%ipv6)
    print ("="*15)

    #ipv6の短縮形，非短縮系の変換
    print ("exploded ipv6 : %s"%ipv6.exploded)
    print ("compressed ipv6 : %s"%ex_ipv6.compressed)
    print ("="*15)

    #リンクローカルアドレスかどうかの判定
    print ("%s is linklocal : %s"%(ipv6,ipv6.is_link_local))

    ipv6_ll = ipaddress.ip_address('fe80::104:1')
    print ("%s is linklocal : %s"%(ipv6_ll,ipv6_ll.is_link_local))