from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import ipaddress
import json
import urllib.request
import sys
import subprocess

app = Flask(__name__)

def checkAzureIp(ipaddr):
    ip = ipaddress.ip_address(ipaddr)
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
    msg = str(ipaddr) + "\n"
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
                        msg += "$" + "\n"
                        IsResult = True
                        break
            
            if IsResult: break
        if IsResult: break
    
    if IsResult != True:
        msg += str(ipaddr) + " does not contain Azure Public IP Addresses." + "\n"
        msg += "$" + "\n"

    res = subprocess.run(["whois",str(ipaddr)], stdout=subprocess.PIPE)
    msg += "$ whois " + str(ipaddr) + "\n" + res.stdout.decode('utf-8') + "\n"
    return msg

@app.route("/", methods=['GET'])
def route():
    return render_template('ccip.html', msg='', ipaddr='')

@app.route("/health", methods=['GET'])
def health():
    return render_template('health.html')

@app.route("/ccip", methods=['GET','POST'])
def ccip():
    if request.method == 'POST':
        if request.method == 'POST':
            if request.form['ipaddr'] is None :
                return render_template('ccip.html', msg='', ipaddr='')
            else:
                ipaddr = request.form['ipaddr']

                try:
                    ipaddress.ip_address(ipaddr)
                    print(ipaddr)
                    msg = checkAzureIp(ipaddr)
                    
                except Exception as e:
                    msg = str(ipaddr) + "\n"
                    msg += str(e)

                return render_template('ccip.html', msg=msg, ipaddr=ipaddr) 
                
    else:
        return render_template('ccip.html', msg='', ipaddr='')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

