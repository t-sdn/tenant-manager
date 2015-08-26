import os
from flask import Flask, render_template, request
from scripts import make_tenant


app = Flask(__name__)

app.config['INTERFACE'] = os.environ['INTERFACE']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/<name>', methods=['POST'])
@app.route('/create/', defaults={'name': None}, methods=['POST'])
def create_tenant(name):
    name = name if name else request.form['name']
    ip = request.form['ip']
    vni = request.form['vni']
    interface = app.config['INTERFACE']
    stdout, stderr = make_tenant(name, ip, vni, interface)

    return render_template('error.html', stdout=stdout, stderr=stderr)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
