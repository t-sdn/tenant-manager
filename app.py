import os
from flask import Flask, render_template, request
from scripts import make_tenant_vlan, make_tenant_vxlan


app = Flask(__name__)

app.config['INTERFACE'] = os.environ['INTERFACE']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/vlan/create/<name>', methods=['POST'])
@app.route('/vlan/create/', defaults={'name': None}, methods=['POST'])
def create_tenant_vlan(name):
    name = name if name else request.form['name']
    ip = request.form['ip']
    vid = request.form['vid']
    interface = app.config['INTERFACE']

    stdout, stderr = make_tenant_vlan(name, ip, vid, interface)
    return render_template('result.html', stdout=stdout, stderr=stderr)


@app.route('/vxlan/create/<name>', methods=['POST'])
@app.route('/vxlan/create/', defaults={'name': None}, methods=['POST'])
def create_tenant_vxlan(name):
    name = name if name else request.form['name']
    ip = request.form['ip']
    vni = request.form['vni']
    interface = app.config['INTERFACE']

    stdout, stderr = make_tenant_vxlan(name, ip, vni, interface)
    return render_template('result.html', stdout=stdout, stderr=stderr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
