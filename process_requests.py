#!/usr/bin/python3

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy 			# http://docs.tweepy.org/en/v3.5.0/ 
import configparser
import argparse



## config
def init(config_file_name):
	config=configparser.ConfigParser()
	config.read(config_file_name)
	CONSUMER_KEY = config['API']['CONSUMER_KEY']
	CONSUMER_SECRET = config['API']['CONSUMER_SECRET']
	ACCESS_TOKEN = config['API']['ACCESS_TOKEN']
	ACCESS_SECRET = config['API']['ACCESS_SECRET']
	return(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN)


# Variables that contains the user credentials to access Twitter API


# Setup tweepy to authenticate with Twitter credentials:
def authenticate(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	# Create the api to connect to twitter with your credentials
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
	return api

#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
# The following loop will print most recent statuses, including retweets, posted by the authenticating user and that users friends. 
# This is the equivalent of /timeline/home on the Web.
#---------------------------------------------------------------------------------------------------------------------
#makes the request and saves result in a log file
def request_log(api):
	outfile = open(args.outfile, "w")
	for status in tweepy.Cursor(api.search,q=('#'+str(args.hashtags[0]))).items(args.N):
		print('w')
		outfile.write(json.dumps(status._json)+"\n")
	outfile.close()

#makes the requests and diplays raw json
def request_print(api):
	for status in tweepy.Cursor(api.home_timeline).items(2):
		print(json.dumps(status._json))

#---------------------------------------------------------------------------------------------------------------------
# Twitter API development use pagination for Iterating through timelines, user lists, direct messages, etc. 
# To help make pagination easier and Tweepy has the Cursor object.
#---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	# Instantiate the parser
	parser = argparse.ArgumentParser(description='python script to request tweets depending on hashtags')
	# Required positional argument
	parser.add_argument('--api', help='required config file with API keys')
	parser.add_argument('-N', type=int,help='number of tweets to monitor')
	parser.add_argument('hashtags', required=True, metavar='#', nargs='+', help='hashtags to browse')
	parser.add_argument('--outfile', help='optionnal output file (json format)')
	args = parser.parse_args()

	print('using config file : '+str(args.api))
	(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN) = init(args.api)
	# print(CONSUMER_SECRET)
	# print(CONSUMER_KEY)
	print('browse hashtags : '+str(args.hashtags))
	if(args.outfile):
		print('outfile : '+str(args.outfile))
		request_log(authenticate(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN))
	else:
		print('no outfile')
		request_print(authenticate(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN))
	