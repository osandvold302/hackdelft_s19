
def saveData(data,name_db):
    s = ''
    for d in data:
        s += str(d['time']) + '\t' + str(d['bidprice']) + '\t' + str(d['askprice']) + '\t' + str(d['bidvol']) + '\t' + str(d['askvol']) + '\n'
    f = open(name_db,'w+')
    f.write(s)
    f.close()

def loadData(name_db):
    lst = []
    f = open(name_db,'r')
    lines = f.read().split('\n')
    f.close()
    for line in lines:
        if line:
            data = {}
            line = line.split('\t')
            data['time'] = line[0]
            data['bidprice'] = float(line[1])
            data['askprice'] = float(line[2])
            data['bidvol'] = float(line[3])
            data['askvol'] = float(line[4])
            lst.append(data)
    return lst

def createChart(data,len_history,chartname):
    if len(data) > len_history:
        chart = {'labels':[],'bidprice':[],'askprice':[],'id':'chart-'+chartname,'name':'chart_'+chartname}
        for d in data[-(len_history+1):-1]:
            chart['labels'].append(d['time'])
            chart['bidprice'].append(d['bidprice'])
            chart['askprice'].append(d['askprice'])

        return chart
    
