import flask
import server_tools as st
from apscheduler.schedulers.background import BackgroundScheduler

history = 60
app = flask.Flask(__name__)
app.secret_key = 'Ry2kv8rNrj9yY3tPRLrmGk3DDoExmr8J'

data_esx = st.loadData('data_esx.txt')
data_sp =  st.loadData('data_sp.txt')

scheduler = BackgroundScheduler()
scheduler.add_job(func=st.saveData, trigger='interval', seconds=60,args=[data_esx,'data_esx.txt'])
scheduler.add_job(func=st.saveData, trigger='interval', seconds=60,args=[data_esx,'data_sp.txt'])
scheduler.start()

@app.route('/')
def MainSite():
    return 'Hello World'

@app.route('/history')
def Dashboard():
    return flask.render_template('dash.html',page='history')

@app.route('/live')
def Live():
    charts = [st.createChart(data_esx,history,'esx'),st.createChart(data_sp,history,'sp')]
    return flask.render_template('live.html',page='live',charts=charts)

@app.route('/upload-data', methods=['POST'])
def updateData():
    time = flask.request.form['time']
    fcode = flask.request.form['fcode']
    bidprice = flask.request.form['bidprice']
    askprice = flask.request.form['askprice']
    bidvol = flask.request.form['bidvol']
    askvol = flask.request.form['askvol']
    if 'SP' in fcode:
        data_sp.append({'time':time,'bidprice':bidprice,'askprice':askprice,'bidvol':bidvol,'askvol':askvol})
    elif 'ESX' in fcode:
        data_esx.append({'time':time,'bidprice':bidprice,'askprice':askprice,'bidvol':bidvol,'askvol':askvol})
    return 'ok'

@app.route('/lst')
def showlst():
    return str(data_esx[-1])

@app.route('/update-sliders/<strdata>')
def UpdateSilders(strdata):
    data = {}
    s = strdata.split(',')
    for t in s:
        t = t.split(':')
        data[t[0]] = float(t[1])
    st.saveSliders(data)
    return 'ok'

@app.route('/crt-update')
def chartUpdate():
    strg = ''
    labels,bid,ask = '','',''
    for d in data_sp[-(history+1):-1]:
        labels += '"'+d['time'] + '";'
        bid += str(d['bidprice']) + ';'
        ask += str(d['askprice']) + ';'
    strg += labels[:-1]+'|'+bid[:-1]+'|'+ask[:-1] + '&&'
    labels,bid,ask = '','',''
    for d in data_esx[-(history+1):-1]:
        labels += '"'+d['time'] + '";'
        bid += str(d['bidprice']) + ';'
        ask += str(d['askprice']) + ';'
    s_ret = strg + labels[:-1]+'|'+bid[:-1]+'|'+ask[:-1]+'&&'
    dx = st.getTableData()
    s_ret += str(dx['position']['ESX_position'])+';'+str(dx['position']['SP_position'])+';'+str(dx['position']['PNL'])+';'+str(dx['position']['PNL_locked'])+';'+str(dx['position']['traded_volume'])+'&&'
    s_ret += str(dx['parameters']['ESX']['mean'])+';'+str(dx['parameters']['ESX']['stdev'])+';'+str(dx['parameters']['ESX']['z-value'])+';'+str(dx['parameters']['ESX']['trade_volume'])+'&&'
    s_ret += str(dx['parameters']['SP']['mean'])+';'+str(dx['parameters']['SP']['stdev'])+';'+str(dx['parameters']['SP']['z-value'])+';'+str(dx['parameters']['SP']['trade_volume'])
    #print(s_ret)
    return s_ret

if __name__ == '__main__':
    app.run()
    
