# Spark-Assignment
Big Data Assignment: Using Twitter's tweet-streaming API, Spark and the Natural Language Toolkit to gather sentiment analysis on certain hashtags



Code for the Spark assignment described in a3.pdf. Part 2 contains a live updating bar graph from the tweet data that is being livestreamed used the twitter API and Spark.


Usage for these files as copied from the README.txt:

Docker1:

docker run -it -v $PWD:/app --name twitter -p 9009:9009 python bash

pip install -U git+https://github.com/tweepy/tweepy.git

python twitter_app.py


Docker2:

docker run -it -v $PWD:/app --link twitter:twitter eecsyorku/eecs4415

pip install textblob

spark-submit spark_app.py

Main directory(or a third docker if you prefer):

pip install matplotlib

python livebar.py


PART ONE:

Run twitter_app.py on docker1
Run spark_app.py on docker2
This will create a tweetdata.csv file in the directory or spark_app.py, an example is included.
Run livebar.py. This will show the live analytics of the data

PART TWO:

Run twitter_app1.py on docker1
Run spark_app1.py on docker2
This will create a tweetdata2.csv file in the directory or spark_app1.py, an example is included.
Run livebar2.py. This will show the live analytics of the data
This data is in percentile form of the three weights of sentimental feeling based on the topic.
