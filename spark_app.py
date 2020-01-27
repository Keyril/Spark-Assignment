from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import sys
import csv

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")
# create spark context with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from spark context, interval size 5 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint for RDD recovery (necessary for updateStateByKey)
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dataStream = ssc.socketTextStream("twitter", 9009)

# split each tweet into words
words = dataStream.flatMap(lambda line: line.split(" "))

# filter the words to get only hashtags
hashtags = words.filter(lambda w: '#' in w)
filtered_tags = hashtags.filter(lambda y: any(word == y for word in ['#Trump', '#ImpeachDonaldTrumpNOW', '#impeachment',
                                                                     '#Trump2020', '#ImpeachmentHearing']))

# map each hashtag to be a pair of (hashtag,1)
hashtag_counts = filtered_tags.map(lambda x: (x, 1))


# adding the count of each hashtag to its last count
def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


# do the aggregation, note that now this is a sequence of RDDs
hashtag_totals = hashtag_counts.updateStateByKey(aggregate_tags_count)


# process a single time interval
def process_interval(time, rdd):
    # print a separator
    print("----------- %s -----------" % str(time))
    try:
        # sort counts (desc) in this time instance and take top 10
        sorted_rdd = rdd.sortBy(lambda x: x[1], False)
        tags = sorted_rdd.take(5)

        # print it nicely
        write_to_csv(tags)
        for tag in tags:
            print('{:<40} {}'.format(tag[0], tag[1]))
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


def write_to_csv(tags):
    with open('tweetdata.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for tag in tags:
            filewriter.writerow([tag[0], tag[1]])
    csvfile.close()


# do this for every single interval
hashtag_totals.foreachRDD(process_interval)

# start the streaming computation
ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
