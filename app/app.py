from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import ipaddress
import utilities.cloudUtility

app = Flask(__name__)

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
                    msg = utilities.cloudUtility.CheckIP(ipaddr)
                    
                except Exception as e:
                    msg = str(ipaddr) + "\n"
                    msg += str(e)

                return render_template('ccip.html', msg=msg, ipaddr=ipaddr) 
                
    else:
        return render_template('ccip.html', msg='', ipaddr='')

@app.route("/cyip", methods=['GET'])
def cyip():
    remoteAddr = request.remote_addr
    xFowarderedFor = request.headers.getlist("X-Forwarded-For")
    xRealIP = request.headers.getlist("X-Real-IP")
    accessRoute = request.access_route
    return render_template('cyip.html', remoteAddr=remoteAddr, xFowarderedFor=xFowarderedFor, xRealIP=xRealIP, accessRoute=accessRoute)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)

