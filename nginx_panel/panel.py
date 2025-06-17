import os
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

NGINX_SITES_AVAILABLE = '/etc/nginx/sites-available'
NGINX_SITES_ENABLED = '/etc/nginx/sites-enabled'


def run_command(cmd):
    """Run shell command and return output."""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return result.stdout.strip()


@app.route('/')
def index():
    status = run_command('systemctl is-active nginx')
    return jsonify({'nginx_status': status})


@app.route('/start', methods=['POST'])
def start_nginx():
    output = run_command('systemctl start nginx')
    return jsonify({'output': output})


@app.route('/stop', methods=['POST'])
def stop_nginx():
    output = run_command('systemctl stop nginx')
    return jsonify({'output': output})


@app.route('/reload', methods=['POST'])
def reload_nginx():
    output = run_command('systemctl reload nginx')
    return jsonify({'output': output})


@app.route('/sites')
def list_sites():
    sites = os.listdir(NGINX_SITES_AVAILABLE)
    return jsonify({'sites': sites})


@app.route('/sites', methods=['POST'])
def add_site():
    data = request.get_json(force=True)
    domain = data.get('domain')
    root_dir = data.get('root')
    if not domain or not root_dir:
        return jsonify({'error': 'domain and root are required'}), 400
    config = f"""
server {{
    listen 80;
    server_name {domain};
    root {root_dir};
    index index.html index.htm;
}}
"""
    conf_path = os.path.join(NGINX_SITES_AVAILABLE, domain)
    with open(conf_path, 'w') as f:
        f.write(config)
    # enable site
    enabled_path = os.path.join(NGINX_SITES_ENABLED, domain)
    if not os.path.exists(enabled_path):
        run_command(f'ln -s {conf_path} {enabled_path}')
    reload_output = run_command('systemctl reload nginx')
    return jsonify({'created': domain, 'reload': reload_output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
