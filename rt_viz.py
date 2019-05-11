from messages import Price, Trade
import matplotlib.pyplot as plt
import socket

plt.subplots(nrows=2, ncols=2, sharex=True)

UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

i=0

while True:
    packet = sock.recvfrom(65535)
    raw_request = str(packet[0])
    
    if "TYPE=PRICE" in raw_request:
        price = Price.from_packet(raw_request)
        print(price.timestamp, price.feedcode, price.bid, price.ask)

    elif "TYPE=TRADE" in raw_request:
        trade = Trade.from_packet(raw_request)
        print(trade.timestamp, trade.feedcode, trade.side, trade.price, trade.volume)
        
    i+=1