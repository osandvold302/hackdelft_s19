# -*- coding: utf-8 -*-
"""Copy of basic_algo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BVyZgun3CKdkBvqs_5B-5dHTvmByAtg8
"""

from messages import Price, Trade
from TradeManager import TradeManager
from utils import read_json
# import json
import numpy as np
import socket, json, time

WINDOW = 20

ESX_list = []
SP_list = []

d = dict()
d["feedcode"] = ""
d["price"] = 0
d["volume"] = 0


def buyOrSell(d, prev_60_val, newval, other_market):
    if other_market == []:
        mean = np.mean(prev_60_val)
        # calculate mean based on queue
        std = np.std(prev_60_val)
        # calculated std
        z = (newval - mean) / std
        # print(z)
        # calculate z-score
        # if z > 2 == negative value (sell)
        if z > 2:
            d["price"] = newval
            d["volume"] = -5
            return d
        # else if z < -2 == positive value (buy)
        elif z < -2:
            d["price"] = newval
            d["volume"] = 5
            return d

        else:
            # return 0 price, 0 volume
            d["volume"] = 0
            return d
    else:
        if len(prev_60_val) <= len(other_market):
            from scipy.stats import spearmanr
            corr, p = spearmanr(other_market[:60],prev_60_val[:60])
            if corr < -0.6:
                d["price"] = newval + (-corr * newval)
                d["volume"] = 5 + int(5 * -corr)
                return d
            corr2, p = spearmanr(prev_60_val[:60],other_market[:60])
            if corr2 < -0.6:
                return buyOrSell(d, other_market, newval, [])
        d["volume"] = 0
        return d



mngr = TradeManager("30_bot_new_ted")

old_ts_esx = None
old_ts_sp = None

while (True):
    json_dict = read_json("recordings/prices.json")  # read the json file
    if json_dict["ESX"][
        "timestamp"] != old_ts_esx:  # if the timestamp is different than the old timestamp we have a new packet
        d["feedcode"] = "ESX"  # so we set the fee
        ESX_list.append(json_dict["ESX"]["bid"]["price"])

        if len(ESX_list) > WINDOW:
            ESX_list.pop(0)  # keep only the WINDOW last values

            # call buyOrSell
            d = buyOrSell(d, ESX_list, json_dict["ESX"]["bid"]["price"], SP_list)
        old_ts_esx = json_dict["ESX"]["timestamp"]

        if d["volume"] != 0:
            json_dict = read_json("recordings/prices.json")

        if d["volume"] > 0:
            d["price"] = json_dict[d["feedcode"]]["ask"]["price"]
            action = "BUY"
        elif d["volume"] < 0:
            d["price"] = json_dict[d["feedcode"]]["bid"]["price"]
            action = "SELL"

        if d["volume"] != 0:
            status = mngr.make_trade(d["feedcode"] + "-FUTURE", action, d["price"], np.abs(d["volume"]))
            print(d, status)
            

    if json_dict["SP"]["timestamp"] != old_ts_sp:
        d["feedcode"] = "SP"
        SP_list.append(json_dict["SP"]["bid"]["price"])

        if len(SP_list) > WINDOW:
            SP_list.pop(0)  # keep only the WINDOW last values

            # call buyOrSell
            d = buyOrSell(d, SP_list, json_dict["SP"]["bid"]["price"],ESX_list)
        old_ts_sp = json_dict["SP"]["timestamp"]

        if d["volume"] != 0:
            json_dict = read_json("recordings/prices.json")

        if d["volume"] > 0:
            d["price"] = json_dict[d["feedcode"]]["ask"]["price"]
            action = "BUY"
        elif d["volume"] < 0:
            d["price"] = json_dict[d["feedcode"]]["bid"]["price"]
            action = "SELL"

        if d["volume"] != 0:
            # print(d)
            status = mngr.make_trade(d["feedcode"] + "-FUTURE", action, d["price"], np.abs(d["volume"]))
            print(d, status)

time.sleep(0.05)