from flask import Flask, Request, Response, jsonify, request, abort
from urllib.parse import urlparse
from flask_cors import CORS
from spider import crawl

app = Flask(__name__)
CORS(app)

jobs = {}

@app.route("/crawl", methods=['POST'])
def hello():
    url = request.form['url']
    depth = request.form['depth']
    # queue the task to celery and provide a job ID
    if urlparse(url).scheme == '':
        url = 'http://' + url
    res = crawl.delay([url], int(depth))
    jobs[res.id] = res
    return jsonify(res.id)

@app.route("/status/<jid>", methods=['GET'])
def check_job_status(jid):
    if jid in jobs:
        return jobs[jid].status
    else:
        return jsonify('Job not found!'), 400

@app.route("/results/<jid>", methods=['GET'])
def get_results(jid):
    if jid in jobs and jobs[jid].status != 'PENDING':
        job = jobs[jid]
        del jobs[jid]
        return Response(response=job.result, mimetype='text/json')
    elif jobs[jid].status == 'PENDING':
        return Response('Job not complete yet!')
    else:
        return jsonify('Job not found!'), 400
