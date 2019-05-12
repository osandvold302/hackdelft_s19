# -*- coding: utf-8 -*-
"""Copy of basic_algo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BVyZgun3CKdkBvqs_5B-5dHTvmByAtg8
"""

from messages import Price, Trade
from TradeManager import TradeManager
from utils import read_json
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

def buyOrSell(d,prev_val, newval):
  mean = np.mean(prev_val)
  # calculate mean based on queue
  std = np.std(prev_val)
  # calculated std
  z = (newval - mean)/ std
  # print(z)
  if np.abs(z) > 2:
    d["price"] = newval
      # d["volume"] = round(math.pow(-5, z-1))
    d["volume"] = int(round(-1*np.sign(z)*np.power(5, np.abs(z)-1)))

    return d
  d["volume"] = 0
  return d

mngr = TradeManager("30_bot_exponent")

old_ts_esx = None
old_ts_sp = None

while(True):
  json_dict = read_json("recordings/prices.json") #read the json file

  if json_dict["ESX"]["timestamp"] != old_ts_esx: # if the timestamp is different than the old timestamp we have a new packet
    d["feedcode"] = "ESX" #so we set the fee
    ESX_list.append(json_dict["ESX"]["bid"]["price"])

    if len(ESX_list)>WINDOW:
      ESX_list.pop(0) # keep only the WINDOW last values

      # call buyOrSell      
      d = buyOrSell(d,ESX_list,json_dict["ESX"]["bid"]["price"])
    old_ts_esx = json_dict["ESX"]["timestamp"]

    if d["volume"] != 0:
      json_dict = read_json("recordings/prices.json")

    if d["volume"] > 0:
      d["price"] = json_dict[d["feedcode"]]["ask"]["price"]
      action = "BUY"
    elif d["volume"] < 0 :
      d["price"] = json_dict[d["feedcode"]]["bid"]["price"]
      action= "SELL"
    
    if d["volume"] != 0:
      # status = mngr.make_trade(d["feedcode"]+"-FUTURE", action, d["price"], np.abs(d["volume"]))
      print(d)

  if json_dict["SP"]["timestamp"] != old_ts_sp:
    d["feedcode"] = "SP"
    SP_list.append(json_dict["SP"]["bid"]["price"])

    if len(SP_list)>WINDOW:
      SP_list.pop(0) # keep only the WINDOW last values

      # call buyOrSell      
      d = buyOrSell(d,SP_list,json_dict["SP"]["bid"]["price"])
    old_ts_sp = json_dict["SP"]["timestamp"]

    if d["volume"] != 0:
      json_dict = read_json("recordings/prices.json")

    if d["volume"] > 0:
      d["price"] = json_dict[d["feedcode"]]["ask"]["price"]
      action = "BUY"
    elif d["volume"] < 0 :
      d["price"] = json_dict[d["feedcode"]]["bid"]["price"]
      action= "SELL"
    
    if d["volume"] != 0:
      # print(d)
      # status = mngr.make_trade(d["feedcode"]+"-FUTURE", action, d["price"], np.abs(d["volume"]))
      print(d)
# time.sleep(0.05)