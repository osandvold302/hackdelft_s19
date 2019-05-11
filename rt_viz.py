from messages import Price, Trade
import matplotlib.pyplot as plt
import socket

fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True)





UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

i=0

SP_price = []
SP_volume = []
SP_timestamp = []

ESX_price = []
ESX_volume = []
ESX_timestamp = []    

# blue is bid, ask is orange
while True:
    packet = sock.recvfrom(65535)
    raw_request = str(packet[0])
    # im really sorry this code exists

    if "TYPE=PRICE" in raw_request:
        price = Price.from_packet(raw_request)

        if price.feedcode == "SP-FUTURE":
            axes[0,0].cla()
            axes[1,0].cla()

            SP_price.append((price.bid[0], price.ask[0]))
            SP_volume.append((price.bid[1], price.ask[1]))
            SP_timestamp.append(price.timestamp.to_datetime64())
            axes[0, 0].set_title("Price SP-FUTURE")
            axes[1, 0].set_title("Volume SP-FUTURE")


            axes[0, 0].plot(SP_timestamp, [i[0] for i in SP_price], color="C0")
            axes[0, 0].plot(SP_timestamp,[i[1] for i in SP_price], color="C1")
            axes[1, 0].plot(SP_timestamp,[i[0] for i in SP_volume], color="C0")
            axes[1, 0].plot(SP_timestamp,[i[1] for i in SP_volume], color="C1")

        if price.feedcode == "ESX-FUTURE":
            axes[0,1].cla()
            axes[1,1].cla()
            
            ESX_price.append((price.bid[0], price.ask[0]))
            ESX_volume.append((price.bid[1], price.ask[1]))
            ESX_timestamp.append(price.timestamp.to_datetime64())

            axes[0, 1].set_title("Price ESX-FUTURE")
            axes[1, 1].set_title("Volume ESX-FUTURE")

            axes[0, 1].plot(ESX_timestamp, [i[0] for i in ESX_price], color="C0")
            axes[0, 1].plot(ESX_timestamp,[i[1] for i in ESX_price], color="C1")
            axes[1, 1].plot(ESX_timestamp, [i[0] for i in ESX_volume], color="C0")
            axes[1, 1].plot(ESX_timestamp,[i[1] for i in ESX_volume], color="C1")
            
        plt.pause(0.0001)

    elif "TYPE=TRADE" in raw_request:
        trade = Trade.from_packet(raw_request)
        
    i+=1