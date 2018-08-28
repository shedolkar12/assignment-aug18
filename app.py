from flask import Flask
from flask import render_template
from flask import request
import requests
import json
import base64
app = Flask(__name__)
GITHUB_BASE_URL = "https://api.github.com"

@app.route('/')
def index():
    return "Welcome to Flask Application!!!"

@app.route('/<username>')
def profile(username):
    url = GITHUB_BASE_URL+'/users/%s'%username
    r = requests.get(url, auth=('shedolkar12', 'Shaddy@12'))
    if r.status_code!=200:
        return "Not Valid User"
    url = GITHUB_BASE_URL + '/users/%s/repos'%username
    repos = requests.get(url, auth=('shedolkar12', 'Shaddy@12'))
    content = r.json()
    content['repos'] = []
    content['username'] = username
    for obj in repos.json():
        d = dict()
        d['name'] = obj['name']
        d['url'] = obj['url']
        d['date_created'] = obj['created_at']
        content['repos'].append(d)
    return render_template('profile.html', **content)

@app.route('/<username>/<repo>')
def repo_master(username=None, repo=None):
    sha = get_master_branch_sha(username, repo)
    if not sha:
        return "No branches"
    trees_url = GITHUB_BASE_URL + '/repos/%s/%s/git/trees/%s'%(username, repo, sha)
    r = requests.get(trees_url, auth=('shedolkar12', 'Shaddy@12'))
    if r.status_code!=200:
        return "Not valid Repo"
    content = r.json()
    return render_template('directory.html', **content)

def get_master_branch_sha(username, repo):
    url = GITHUB_BASE_URL + '/repos/%s/%s/branches'%(username, repo)
    r = requests.get(url, auth=('shedolkar12', 'Shaddy@12'))
    if r.status_code!=200:
        return "Not Valid"
    response = r.json()
    sha = None
    for obj in response:
        if obj['name']=='master':
            sha = obj['commit']['sha']
    return sha

@app.route('/tree/<typ>/<path>')
def directory(typ=None, path=None):
    trees_url = request.args.get('url', None)
    r = requests.get(trees_url, auth=('shedolkar12', 'Shaddy@12'))
    if r.status_code!=200:
        return "Not valid Repo"
    if typ=='tree':
        content = r.json()
        return render_template('directory.html', **content)
    elif typ=="blob":
        typ = 'other'
        exte = path.split('.')[-1]
        if exte.lower() in ['jpeg', 'png', 'jpg']:
            typ = 'img'
            content = r.json()['content']
        else:
            content =  base64.b64decode(r.json()['content'])
        return render_template("file.html", content=content, typ=typ)
    else:
        return "Not valid type"

if __name__ == '__main__':
    app.run()
