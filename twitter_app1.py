import socket
import sys
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream

# Replace the values below with yours
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
hashtags = [
    '#Trump', '#ImpeachDonaldTrumpNOW', '#impeachment', '#Trump2020', '#ImpeachmentHearing',
    '#DonaldTrump', '#Republican', '#Democrat', '#VoteBlue', '#MAGA',
    '#HongKong', '#HongKongProtests', '#HongKongPoliceTerrorist', '#StandwithHK', '#FreedomHongKong',
    '#StandWithHongKong', '#HongKongPoliceBrutality', '#SOSHongKong', '#HK', '#HKPolice',
    '#Iran', '#Internet4Iran', '#IranProtests', '#IranProtestors', '#Iranian',
    '#IranianProtests', '#KeepItOn', '#FreeInternetForIran', '#IraniansWantRegimeChange', '#IranUprising',
    '#ChickFilA', '#BoycottChickFilA', '#Popeyes', '#SalvationArmy', '#NoChickFilA',
    '#ByeChickFilA', '#FuckChickFilA', '#FuckPopeyes', '#ChickenSandwichWars', '#PopeyesChickenSandwich',
    '#Climate', '#ClimateChange', '#ClimateAction', '#ClimateChaneIsReal', '#TeamTrees',
    '#ClimateCrisis', '#ActOnClimate', '#PriceOnPollution', '#ClimateTwitter', '#ClimateActionNow',
            ]


class TweetListener(StreamListener):
    def on_data(self, data):
        try:

            global conn

            # load the tweet JSON, get pure text
            full_tweet = json.loads(data)
            tweet_text = full_tweet['text']
            # print the tweet plus a separator
            print("------------------------------------------")
            print(tweet_text + '\n')

            # send it to spark
            if any(word in tweet_text for word in hashtags[0:10]):
                conn.send(str.encode('Trump' + '\t' + tweet_text + '\n'))
            if any(word in tweet_text for word in hashtags[10:20]):
                conn.send(str.encode('HongKong' + '\t' + tweet_text + '\n'))
            if any(word in tweet_text for word in hashtags[20:30]):
                conn.send(str.encode('Iran' + '\t' + tweet_text + '\n'))
            if any(word in tweet_text for word in hashtags[30:40]):
                conn.send(str.encode('ChickFilA' + '\t' + tweet_text + '\n'))
            if any(word in tweet_text for word in hashtags[40:50]):
                conn.send(str.encode('Climate' + '\t' + tweet_text + '\n'))
        except:

            # handle errors
            e = sys.exc_info()[0]
            print("Error: %s" % e)

        return True

    def on_error(self, status):
        print(status)


# ==== setup local connection ====

# IP and port of local machine or Docker
TCP_IP = socket.gethostbyname(socket.gethostname())  # returns local IP
TCP_PORT = 9009

# setup local connection, expose socket, listen for spark app
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Waiting for TCP connection...")

# if the connection is accepted, proceed
conn, addr = s.accept()
print("Connected... Starting getting tweets.")

# ==== setup twitter connection ====
listener = TweetListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, listener)

# setup search terms
language = ['en']

# get filtered tweets, forward them to spark until interrupted
try:
    stream.filter(track=hashtags, languages=['en'])
except KeyboardInterrupt:
    s.shutdown(socket.SHUT_RD)
