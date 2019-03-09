# DUMBO 

python3 script for listening to twitter hashtags
forked from the tutorial [here, by Wei XU](http://socialmedia-class.org/twittertutorial.html).
forked analysis tool from x0rz here : https://github.com/x0rz/tweets_analyzer"

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
### get tweets :
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
### parse and display tweets :
```
usage: parsetweets.py [-h] [--infile INFILE]

python script to parse tweets requested

optional arguments:
  -h, --help       show this help message and exit
  --infile INFILE  required input file (json format)
```

### analyze a profile
from x0rz : https://github.com/x0rz/tweets_analyzer
```
usage: profiler.py [-h] --api API [--tweets_nb TWEETS_NB]
                   [--timezone_offset TIMEZONE_OFFSET] [--no-color] [--save]
                   profile

python script to analyze a profile

positional arguments:
  profile               target profile name to analyze

optional arguments:
  -h, --help            show this help message and exit
  --api API             required config file with API keys (ex : --api
                        ../config.ini)
  --tweets_nb TWEETS_NB
                        number of tweets to monitor (default=1000)
  --timezone_offset TIMEZONE_OFFSET
                        Offset to UTC (ex : for Paris (UTC+1)
                        --timezone_offset 1
  --no-color            disables colored output
  --save                file to save json
```