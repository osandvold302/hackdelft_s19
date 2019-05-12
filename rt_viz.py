from messages import Price, Trade
import matplotlib.pyplot as plt
import socket
import requests

plt.subplots(nrows=2, ncols=2, sharex=True)
sess = requests.Session()
url = 'http://127.0.0.1:5000/upload-data'





UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

i=0


# blue is bid, ask is orange
while True:
    packet = sock.recvfrom(65535)
    raw_request = str(packet[0])
    # im really sorry this code exists

    if "TYPE=PRICE" in raw_request:
        price = Price.from_packet(raw_request)
        print(price.timestamp, price.feedcode, price.bid, price.ask)
        data = {'time':price.timestamp,'fcode':price.feedcode,'bidprice':price.bid[0],'bidvol':price.bid[1],'askprice':price.ask[0],'askvol':price.ask[1]}
        sess.post(url,data=data)
    elif "TYPE=TRADE" in raw_request:
        trade = Trade.from_packet(raw_request)
        #print(trade.timestamp, trade.feedcode, trade.side, trade.price, trade.volume)
        
    i+=1
    
