from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<n>')
def hello_name(n):
    return "Hello {}!".format(n)

@app.route('/test/<name>/')
def hello1(name=None):
    return render_template('test.html', name=name)

if __name__ == '__main__':
    app.run()
