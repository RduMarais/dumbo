# DUMBO 

python3 script for listening to twitter hashtags
forked from the tutorial [here, bei Wei XU](http://socialmedia-class.org/twittertutorial.html).

## dependencies
install python library tweepy using pip : (use pip3 for disambiguation, since we use python3)
`pip install tweepy`

## configuration
put in a config file your API keys as : 

```
[API]
consumer_key = <THE_CONSUMER_KEY>
consumer_secret = <THE_CONSUMER_SECRET_KEY>
access_secret = <THE_ACCESS_SECRET_KEY>
access_token = <THE_ACCESS_TOKEN>
```

## usage
```
usage: try_tweepy.py [-h] [--api API] [--outfile OUTFILE] # [# ...]

python script to request tweets depending on hashtags

positional arguments:
  #                  hashtags to browse

optional arguments:
  -h, --help         show this help message and exit
  --api API          required config file with API keys, ex : --api ../config.ini
  --outfile OUTFILE  optionnal output file (json format)
```
