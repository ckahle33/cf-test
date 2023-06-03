import os
import requests
from dotenv import load_dotenv

from flask import Flask, request, render_template, jsonify, make_response

app = Flask(__name__)

load_dotenv()

cloudflare_base_url = 'https://api.cloudflare.com/client/v4/'
api_token = os.getenv('CF_API_KEY')
zone_id = os.getenv('CF_ZONE_ID')

@app.route("/")
def index():

    headers = dict(request.headers)
    if request.headers.get('Content-Type') == 'application/json':
        return make_response(jsonify(headers), 200) 
    else:
        return render_template("index.html", headers=headers)
    
@app.route("/headers")
def headers():

    headers = dict(request.headers)
    if request.headers.get('Content-Type') == 'application/json':
        return make_response(jsonify(headers), 200) 
    else:
        return render_template("headers.html", headers=headers)
    

@app.route("/dns")
def dns():
    headers = {"Authorization": "Bearer " + api_token, "Content-Type": "application/json"}
    url = cloudflare_base_url + 'zones/{zone_id}/dns_records'.format(zone_id=zone_id)
    print(url)
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

@app.route("/worker")
def worker():
    return render_template("worker.html")

@app.route("/secure")
def secure():
    return render_template("secure.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))