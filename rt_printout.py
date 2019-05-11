from messages import Price, Trade
import socket
import os

UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))



ESX = { "bid" : (0,0),
        "ask" : (0,0)}

SP = { "bid" : (0,0),
        "ask" : (0,0)}


while True:
    packet = sock.recvfrom(65535)
    raw_request = str(packet[0])
    # im really sorry this code exists

    if "TYPE=PRICE" in raw_request:
        price = Price.from_packet(raw_request)

        if price.feedcode == "SP-FUTURE":
            SP["bid"] = price.bid
            SP["ask"] = price.ask

        if price.feedcode == "ESX-FUTURE":
            ESX["bid"] = price.bid
            ESX["ask"] = price.ask

        timestamp = price.timestamp

        os.system('cls' if os.name == 'nt' else 'clear')
        print("""\n\n\n\n
                SP-FUTURE\t\t\t\t|           ESX-FUTURE
                PRICE\t\tVOLUME\t\t\t|           PRICE\t\tVOLUME
            BID {}\t\t{}\t\t\t|       BID {}\t\t{}
            ASK {}\t\t{}\t\t\t|       ASK {}\t\t{}
        \n\n
            TIMESTAMP {}""".format(SP["bid"][0], SP["bid"][1], ESX["bid"][0], ESX["bid"][1],SP["ask"][0], SP["ask"][1], ESX["ask"][0], ESX["ask"][1], timestamp))
        