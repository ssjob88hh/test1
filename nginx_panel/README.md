# Simple Nginx Control Panel

This is a minimal Flask-based control panel for managing Nginx on Ubuntu.
It exposes HTTP endpoints to start, stop and reload the Nginx service as well
as create new server blocks automatically.

## Features
- View Nginx service status
- Start, stop and reload Nginx
- List available server blocks
- Create new server blocks on the fly

## Requirements
- Python 3.11+
- `flask` Python package
- Root privileges to manage Nginx

Install dependencies with:
```bash
pip install flask
```

## Running
```bash
sudo python3 panel.py
```
The application listens on port `8080`.

## Example requests
Check service status:
```bash
curl http://localhost:8080/
```
Create a new site:
```bash
curl -X POST -H 'Content-Type: application/json' \
     -d '{"domain": "example.com", "root": "/var/www/example"}' \
     http://localhost:8080/sites
```
