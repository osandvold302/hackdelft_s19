import flask

app = flask.Flask(__name__)
app.secret_key = 'Ry2kv8rNrj9yY3tPRLrmGk3DDoExmr8J'

@app.route('/')
def MainSite():
    return 'Hello World'

@app.route('/dash')
def Dashboard():
    return flask.render_template('dash.html')


if __name__ == '__main__':
    app.run()
