from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import sys
import csv
import re
from textblob import TextBlob

# data structures for topics
# index, pos, neu, neg, count
topics = [
    ['Trump', 0, 0, 0, 0],
    ['HongKong', 0, 0, 0, 0],
    ['Iran', 0, 0, 0, 0],
    ['ChickFilA', 0, 0, 0, 0],
    ['Climate', 0, 0, 0, 0]
]

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 5 seconds
ssc = StreamingContext(sc, 1)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter", 9009)


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())


# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    try:
        text_val = rdd.take(1)                                  # get tweet package
        if len(text_val):                                       # check if empty on this interval
            index_text = text_val[0].split('\t')                # split into index and tweet
            print(index_text[1])                                # print tweet
            analysis = TextBlob(clean_tweet(index_text[1]))     # clean tweet
            polarity = analysis.sentiment.polarity              # get tweet polarity
            update_lists(polarity, index_text[0])               # update data structures representing the topics
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


def update_lists(polarity, index):
    i = 4
    if index == topics[0][0]:
        i = 0
    elif index == topics[1][0]:
        i = 1
    elif index == topics[2][0]:
        i = 2
    elif index == topics[4][0]:
        i = 3
    else:
        i = 4
    topics[i][4] += 1
    if polarity > 0:
        topics[i][1] += 1  # positive
    elif polarity == 0:
        topics[i][2] += 1  # neutral
    else:
        topics[i][3] += 1  # negative
    write_to_csv()


def write_to_csv():
    with open('tweetdata2.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Topic', 'Positive', 'Neutral', 'Negative', 'Count'])
        for topic in topics:
            filewriter.writerow([topic[0], topic[1], topic[2], topic[3], topic[4]])
    csvfile.close()


# do this for every single interval
dataStream.foreachRDD(process_interval)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
