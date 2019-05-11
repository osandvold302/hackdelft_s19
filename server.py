import flask

app = flask.Flask(__name__)
app.secret_key = 'Ry2kv8rNrj9yY3tPRLrmGk3DDoExmr8J'

@app.route('/')
def MainSite():
    return 'Hello World'

@app.route('/history')
def Dashboard():
    return flask.render_template('dash.html',page='history')

@app.route('/live')
def Live():
    return flask.render_template('live.html',page='live')

@app.route('/upload-data' methods=['POST'])
def updateData():
    
    

if __name__ == '__main__':
    app.run(
)
    
