# -*- coding: utf-8 -*-
"""Copy of basic_algo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BVyZgun3CKdkBvqs_5B-5dHTvmByAtg8
"""

from messages import Price, Trade
from TradeManager import TradeManager
import math
#import json
import numpy as np
import socket, json
#packet = "TYPE=TRADE|FEEDCODE=SP-FUTURE|SIDE=ASK|PRICE=533.3|VOLUME=122"

#trade = Trade.from_packet(packet)
#print(trade.side)

# 2 queues of length 60
WINDOW = 60

ESX_list = []
SP_list = []

d = dict()
d["feedcode"] = ""
d["price"] = 0
d["volume"] = 0

# hacky way to get around collection
collect_ESX = False
collect_SP = False

def buyOrSell(d,prev_val, newval):
  mean = np.mean(prev_val)
  # calculate mean based on queue
  std = np.std(prev_val)
  # calculated std
  z = (newval - mean)/ std
  # print(z)
  # calculate z-score, compute volume by power of std
  # if z > 2 == negative value (sell)
  if z > 2:
    d["price"] = newval
    d["volume"] = round(math.pow(-5, z-1))
    return d
  # else if z < -2 == positive value (buy)
  elif z < -2:
    d["price"] = newval
    d["volume"] = round(math.pow(5,abs(z)-1))
    return d
  
  else:
    # return 0 price, 0 volume
    d["volume"] = 0
    return d

UDP_IP = "188.166.115.7"
UDP_PORT = 7001
MESSAGE = b"TYPE=SUBSCRIPTION_REQUEST"

sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

mngr = TradeManager("30_bot_simple")

while(True):
  packet = sock.recvfrom(65535)
  raw_request = str(packet[0])

  if "TYPE=TRADE" in raw_request:
    trade = Trade.from_packet(raw_request)
    # If price is ESX  
    if trade.feedcode == "ESX-FUTURE":
      d["feedcode"] = "ESX"
      # Fill until we reach the first 60
      ESX_list.append(trade.price)
      if len(ESX_list)>WINDOW:
        ESX_list.pop(0)
        # call buyOrSell      
        d = buyOrSell(d,ESX_list,trade.price)
    elif trade.feedcode == "SP-FUTURE":
      d["feedcode"] = "SP"
      # Fill until we reach the first 60
      SP_list.append(trade.price)
      if len(SP_list)>WINDOW:
        SP_list.pop(0)
        # call buyOrSell      
        d = buyOrSell(d,SP_list,trade.price)
    if d["volume"] != 0:
      with open("current.json","r") as file:
        json_raw = file.readlines()[0]
        json_dict = json.loads(json_raw)
    
    if d["volume"] > 0:
      d["price"] = json_dict[d["feedcode"]]["ask"]["price"]
      action = "BUY"
    elif d["volume"] < 0 :
      d["price"] = json_dict[d["feedcode"]]["bid"]["price"]
      action= "SELL"
    
    if d["volume"] != 0:
      print(d)
      mngr.make_trade(d["feedcode"]+"-FUTURE", action, d["price"], np.abs(d["volume"]))
