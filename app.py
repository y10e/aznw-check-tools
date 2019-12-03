from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import ipaddress
import json
import urllib.request

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
    msg = ''

    for region in json_dict :
        if json_dict[region] is not None:
            for network in json_dict[region]:
                #print(str(network))
                nw = ipaddress.ip_network(network)

                for addr in nw:
                    if addr == ip:
                        msg = str(ip) + " in " + str(nw) + "(" + str(region) + ")"
                        print(msg)
                        break
            
            if msg is not None: break
        if msg is not None: break
    
    if msg == '':
        print(111)
        msg = "'" + str(ipaddr) + "' does not contain Azure Public IP Addresses." 
        print(msg)

    print(111)
    return msg

@app.route("/", methods=['GET','POST'])
def route():
    if request.method == 'POST':
        if request.method == 'POST':
            
            ipaddr = request.form['ipaddr']
            print(ipaddr)
            msg = checkAzureIp(ipaddr)
            return render_template('index.html', msg=msg) 
    else:
        return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html', msg='') 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

