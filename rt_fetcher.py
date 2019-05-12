from messages import Price, Trade
import socket
import os
import json

def fetch_data(printing=False):
    UDP_IP = "188.166.115.7"
    UDP_PORT = 7001
    MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP

    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))



    ESX = { "bid" : {'price' : 0, 'volume' : 0},
            "ask" : {'price' : 0, 'volume' : 0},
            "timestamp" : 0}

    SP = { "bid" : {'price' : 0, 'volume' : 0},
            "ask" : {'price' : 0, 'volume' : 0},
            "timestamp" : 0}

    pricesDict = { "ESX" : ESX,
                "SP" : SP}

    while True:
        packet = sock.recvfrom(65535)
        raw_request = str(packet[0])
        # im really sorry this code exists

        if "TYPE=PRICE" in raw_request:
            price = Price.from_packet(raw_request)

            if price.feedcode == "SP-FUTURE":
                SP["bid"]["price"] = price.bid[0]
                SP["bid"]["volume"] = price.bid[1]

                SP["ask"]["price"] = price.ask[0]
                SP["ask"]["volume"] = price.ask[1]

                SP["timestamp"] = str(price.timestamp)
            if price.feedcode == "ESX-FUTURE":
                ESX["bid"]["price"] = price.bid[0]
                ESX["bid"]["volume"] = price.bid[1]

                ESX["ask"]["price"] = price.ask[0]
                ESX["ask"]["volume"] = price.ask[1]

                ESX["timestamp"] = str(price.timestamp)

            if printing:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("""\n\n\n\n
                        SP-FUTURE\t\t\t\t|           ESX-FUTURE
                        PRICE\t\tVOLUME\t\t\t|           PRICE\t\tVOLUME
                    BID {}\t\t{}\t\t\t|       BID {}\t\t{}
                    ASK {}\t\t{}\t\t\t|       ASK {}\t\t{}
                    TIMESTAMP {}\t|       TIMESTAMP {}""".format(SP["bid"]["price"], SP["bid"]["volume"], ESX["bid"]["price"], ESX["bid"]["volume"],SP["ask"]["price"], SP["ask"]["volume"], ESX["ask"]["price"], ESX["ask"]["volume"], SP["timestamp"], ESX["timestamp"]))
            
            dump = json.dumps(pricesDict)

            with open("recordings/prices.json", "w") as f:
                f.write(dump)

if __name__ == "__main__":
    fetch_data(printing=True)