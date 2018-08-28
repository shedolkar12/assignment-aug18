from flask import Flask
from flask import render_template
import requests
import json
app = Flask(__name__)
GITHUB_BASE_URL = "https://api.github.com"

@app.route('/')
def index():
    return "Welcome to Flask Application!!!"

@app.route('/<username>')
def profile(username):
    url = GITHUB_BASE_URL+'/users/%s'%username
    r = requests.get(url, auth=('shedolkar12', 'Shaddy@12'))
    url = GITHUB_BASE_URL + '/users/%s/repos'%username
    repos = requests.get(url, auth=('shedolkar12', 'Shaddy@12'))
    content = r.json()
    content['repos'] = []
    for obj in repos.json():
        d = dict()
        d['name'] = obj['name']
        d['url'] = obj['url']
        d['date_created'] = obj['created_at']
        content['repos'].append(d)
    return render_template('profile.html', **content)

@app.route('/<n>')
def hello_name(n):
    return "Hello {}!".format(n)

@app.route('/test/<name>/')
def hello1(name=None):
    return render_template('test.html', name=name)

if __name__ == '__main__':
    app.run()
