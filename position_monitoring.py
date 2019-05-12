import pandas as pd
import csv, requests, datetime, time, json

from TradeManager import TradeManager

def monitor(username, filename, listening_time=3600): #in seconds
    recording = {}
    initTime = pd.Timestamp.utcnow()
    mngr = TradeManager(username=username)
    while pd.Timestamp.utcnow() - initTime < datetime.timedelta(seconds=listening_time):
        timestamp = pd.Timestamp.utcnow()
        status = mngr.get_status()

        recording[str(timestamp)] = status

        dump = json.dumps(recording)
        print(status)
        with open(filename, "w") as f:
            f.write(dump)

        time.sleep(10)

def fetch(usernames):
    mngr = TradeManager(username=usernames[0])

    while True:
        for username in usernames:
            timestamp = pd.Timestamp.utcnow()
            status = mngr.get_status(username=username)

            print(username, status)

            dump = json.dumps(status)
            with open("recordings/position_{}.json".format(username), "w") as f:
                f.write(dump)

        time.sleep(10)

if __name__ == "__main__":
    # monitor("30_bot_simple", "recordings/30_bot_simple.json", listening_time=30*60)
    fetch(["30_bot_simple", "30_bot_exponent"])