import requests
import numpy as np
import socket
import csv

POSITION = "http://188.166.115.7/data/pnls.csv"

UDP_IP = "188.166.115.7"
UDP_PORT = 8001


sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
class TradeError(Exception):
    pass

class TradeManager:
    def __init__(self, username):
        self.username = username
        


    def get_status(self, username=None):
        """Reads the status of a user from the dashboard
        
        Keyword Arguments:
            username {[str]} -- [description] (default: the username associated with the TradeManager)
        
        Returns:
            status [dict] -- Dict containing the position and details about a user
        """
        if username == None:
            username = self.username    
        
        tries = 0
        succesful = False

        while tries<5 and not succesful:
            try:
                with requests.Session() as s:
                    download = s.get(POSITION)
                succesful = True
            except:
                tries+=1
                print(tries)
            
        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=';')

        raw_list = list(cr)[:-1] #last line is empty so we remove it

        usernames = [i[0] for i in raw_list]

        idx = usernames.index(username)

        status = {"PNL" : raw_list[idx][1],
                  "PNL_locked" : raw_list[idx][2],
                  "traded_volume" : raw_list[idx][3],
                  "ESX_position" : raw_list[idx][4],
                  "SP_position" : raw_list[idx][5],
                  }

        return status

    def make_trade(self, feedcode, action, price, volume):
        if action not in ["BUY", "SELL"]:
            raise ValueError("The actions is neither buying nor selling")
        if feedcode not in ["SP-FUTURE", "ESX-FUTURE"]:
            raise ValueError("Check yo feedcode")
        # if not type(price)=="float" or not type(volume)=="int":
            # raise TypeError("Check your numerical values")

        request = "TYPE=ORDER|USERNAME={}|FEEDCODE={}|ACTION={}|PRICE={}|VOLUME={}".format(self.username, feedcode,action,str(price), str(volume))

        sock.sendto(bytes(request,"utf-8"), (UDP_IP, UDP_PORT)) #sending the trade request

        packet = sock.recvfrom(65535) #recieiving feedback
        raw_request = str(packet[0])

        print(raw_request)
        fields = str(raw_request).split("|")

        # error catching in the trade
        if "ERROR=" in raw_request:
            message = fields[1].replace("ERROR=", '')
            raise TradeError(message)
        
        elif "TRADED_VOLUME=0" in raw_request:
            return "NOTRADE"
        
        price = float(fields[2].replace("PRICE=", ''))
        volume = int(fields[3].replace("TRADED_VOLUME=", '').replace('\'', ''))

        return price,volume

if __name__ == "__main__":
    mngr = TradeManager("Group30_test")
    print(mngr.get_status())
    # while True:
    # status = "NOTRADE"
    # while status == "NOTRADE":
    #     status = mngr.make_trade("SP-FUTURE", "BUY", 3091., 1)
    #     print(status)
    
    