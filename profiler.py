#!/usr/bin/python3
#
# forked from x0rz : https://github.com/x0rz/tweets_analyzer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# from __future__ import unicode_literals
import tweepy 			# http://docs.tweepy.org/en/v3.5.0/ 
import configparser
import argparse

import sys #for colors
import datetime
import numpy #but may have done without
from tqdm import tqdm



## GLOBALS ??
# Here are sglobals used to store data - I know it's dirty, whatever
start_date = 0
end_date = 0
export = ""
jsono = {}
save_folder = "tweets"
# color_supported = True
# ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
out_json=False


# Setup tweepy to authenticate with Twitter credentials:
def authenticate(configfile):
	(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN) = init(configfile)
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	# Create the api to connect to twitter with your credentials
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
	return api

## READ confi file and set Auth variables
def init(config_file_name):
	config=configparser.ConfigParser()
	config.read(config_file_name)
	CONSUMER_KEY = config['API']['CONSUMER_KEY']
	CONSUMER_SECRET = config['API']['CONSUMER_SECRET']
	ACCESS_TOKEN = config['API']['ACCESS_TOKEN']
	ACCESS_SECRET = config['API']['ACCESS_SECRET']
	return(CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN)

## color printing if not specified without
def supports_color():
	if args.no_color:
		return False
	# copied from https://github.com/django/django/blob/master/django/core/management/color.py
	plat = sys.platform
	supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
	# isatty is not always implemented, #6223.
	is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
	if not supported_platform or not is_a_tty:
		return False
	return True

# Colored print by x0rz : https://github.com/x0rz/tweets_analyzer
def cprint(strng):
	if not color_supported:
		strng = ansi_escape.sub('', strng)
	if out_json is False:
		print(strng)
		export_string(strng)

def print_user_info(user_info):
	print("[+] languague 		: \033[1m%s\033[0m" % user_info.lang)
	print("[+] geo_enabled		: \033[1m%s\033[0m" % user_info.geo_enabled)
	print("[+] time_zone	  	: \033[1m%s\033[0m" % user_info.time_zone)

	print("[+] statuses_count 	: \033[1m%s\033[0m" % user_info.statuses_count)

	if user_info.utc_offset is None:
		print("[\033[91m!\033[0m] Can't get specific timezone for this user")
	else:
		print("[+] utc_offset	 	: \033[1m%s\033[0m" % user_info.utc_offset)

def tweets_to_retrieve(tweets_nb):
	# Will retreive all Tweets from account (or max limit)
	if(args.tweets_nb is None):
		nb_tweets=1000
	else:
		nb_tweets = args.tweets_nb
	num_tweets = numpy.amin([nb_tweets, tweets_nb])
	print("[+] Retrieving last %d tweets..." % num_tweets)
	jsono['status_retrieving'] = num_tweets
	return num_tweets


def process_tweet(status):
	global start_date
	global end_date

# Download tweets by x0rz
def get_tweets(api, username, fh, limit):
	""" Download Tweets from username account """
	if out_json is False:
		for status in tqdm(tweepy.Cursor(api.user_timeline, screen_name=username).items(limit), unit="tw", total=limit):
			process_tweet(status)
			if args.save:
				fh.write(str(json.dumps(status._json))+",")
	else:
		for status in (tweepy.Cursor(api.user_timeline, screen_name=username).items(limit)):
			process_tweet(status)
			if args.save:
				fh.write(str(json.dumps(status._json))+",")

if __name__ == '__main__':
	# Instantiate the parser
	parser = argparse.ArgumentParser(description='python script to analyze a profile')
	# Required positional argument
	parser.add_argument('--api', required=True,help='required config file with API keys (ex : --api ../config.ini)')
	parser.add_argument('--tweets_nb', type=int, help='number of tweets to monitor (default=1000)')
	parser.add_argument('profile', help='target profile name to analyze')
	parser.add_argument('--timezone_offset', type=int, help='Offset to UTC (ex : for Paris (UTC+1) --timezone_offset 1')
	parser.add_argument('--no-color', action='store_true',help='disables colored output')
	parser.add_argument('--save', action='store_true',help='file to save json')

	args = parser.parse_args()
	print('###############################################################################################')
	print('					Python Twitter Profiler')
	print('###############################################################################################')
	print('using config file : '+str(args.api))
	# (CONSUMER_SECRET,CONSUMER_KEY,ACCESS_SECRET,ACCESS_TOKEN) = init(args.api)
	print('analyze profile : '+str(args.profile))

	global color_supported
	color_supported = supports_color()

	twitter_api = authenticate(args.api)

	now = datetime.datetime.now()



	jsono['user_name'] = args.profile
	user_info = twitter_api.get_user(screen_name=args.profile)

	print_user_info(user_info)
	jsono['user_lang'] = user_info.lang
	jsono['user_geo_enabled'] = user_info.geo_enabled
	jsono['user_time_zone'] = user_info.time_zone
	jsono['user_utc_offset'] = user_info.utc_offset
	jsono['status_count'] = user_info.statuses_count

	if args.timezone_offset:
		print("[\033[91m!\033[0m] Applying timezone offset "+str(args.timezone_offset)+" (--timezone-offset)")
		jsono['user_utc_offset_set'] = "Applying timezone offset %d (--utc-offset)" % args.timezone_offset

	nb_tweets = tweets_to_retrieve(user_info.statuses_count)

	save_path = "tweets/"+args.profile
	save_file=False
	if args.save:
		 if not os.path.exists(save_path):
			  os.makedirs(save_path)
		 save_file = open(save_path+"/"+now.strftime("%Y-%m-%d_%H-%M-%S")+".json","w")
		 save_file.write("[")


	# Download tweets
	print("[+] Downloaded %d tweets" % nb_tweets)
	get_tweets(twitter_api, args.profile, save_file, limit=nb_tweets)
	jsono['status_start_date'] = "%s" % start_date
	jsono['status_end_date'] = "%s" % end_date
	jsono['status_days'] = "%s" % (end_date - start_date).days

	if args.save:
		save_file.seek(-1, os.SEEK_END) # drop last ,
		save_file.truncate()
		save_file.write("]")
		save_file.close()



# TODO
	# try:
	# 	main()
	# except tweepy.error.TweepError as e:
	# 	cprint("[\033[91m!\033[0m] Twitter error: %s" % e)
	# except Exception as e:
	# 	cprint("[\033[91m!\033[0m] Error: %s" % e)