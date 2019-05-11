import pandas as pd

class Price:
    def __init__(self, feedcode, bid, ask):
        self.feedcode = feedcode
        self.bid = bid # (price, volume)
        self.ask = ask # tuple containing (price, volume)
        self.timestamp = pd.Timestamp.utcnow()

    @classmethod
    def from_packet(cls, packet):
        fields = str(packet).split("|")

        feedcode = fields[1].replace("FEEDCODE=", '')
        bid_price = float(fields[2].replace("BID_PRICE=", ''))
        bid_volume = float(fields[3].replace("BID_VOLUME=", ''))

        ask_price = float(fields[4].replace("ASK_PRICE=", ''))
        ask_volume = float(fields[5].replace("ASK_VOLUME=", '').replace('\'', ''))
        
        return cls(feedcode, (bid_price, bid_volume), (ask_price, ask_volume))
    
    def append_to_df(self, dataframe):
        pass
    
class Trade:
    def __init__(self, feedcode, side, price, volume):
        self.feedcode = feedcode
        self.side = side
        self.price = price
        self.volume = volume
        self.timestamp = pd.Timestamp.utcnow()

    @classmethod
    def from_packet(cls, packet):
        fields = str(packet).split("|")

        feedcode = fields[1].replace("FEEDCODE=", '')
        side = fields[2].replace("SIDE=", '')
        price = float(fields[3].replace("PRICE=", ''))
        volume = float(fields[4].replace("VOLUME=", '').replace('\'', ''))
        
        return cls(feedcode, side, price, volume)
    
    def append_to_df(self, dataframe):
        pass
    