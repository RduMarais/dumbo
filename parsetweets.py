#!/usr/bin/python3

# Import the necessary package to process data in JSON format
import json
import argparse


# We use the file saved from last step as example
tweets_filename = 'people.json'
tweets_file = open(tweets_filename, "r")

def print_tweets(fileobj):
    for line in tweets_file:
        try:
            # Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet: # only messages contains 'text' field is a tweet
                print(tweet['id']) # This is the tweet's id
                print(tweet['created_at']) # when the tweet posted
                print(tweet['text']) # content of the tweet
                            
                print(tweet['user']['id']) # id of the user who posted the tweet
                print(tweet['user']['name']) # name of the user, e.g. "Wei Xu"
                print(tweet['user']['screen_name']) # name of the user account, e.g. "cocoweixu"

                hashtags = []
                for hashtag in tweet['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                print(hashtags)

        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue

def print_light(fileobj):
    for line in tweets_file:
        try:
            # Read in one line of the file, convert it into a json object 
            tweet = json.loads(line.strip())
            if 'text' in tweet: # only messages contains 'text' field is a tweet
                print("id : "+str(tweet['id'])) # This is the tweet's id
                print("created : " + str(tweet['created_at'])) # when the tweet posted
                print("text : "+str(tweet['text'])) # content of the tweet
                            
                # print(tweet['user']['id']) # id of the user who posted the tweet
                print("user : "+str(tweet['user']['name'])+" | aka "+str(tweet['user']['screen_name'])) # name of the user, e.g. "Wei Xu"

                hashtags = []
                for hashtag in tweet['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                print("# : "+str(hashtags))

        except:
            # read in a line is not in JSON format (sometimes error occured)
            continue    

if __name__ == '__main__':
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='python script to parse tweets requested')
    parser.add_argument('--infile', help='required input file (json format)')
    args = parser.parse_args()

    print('using config file : '+str(args.api))
    print_light(args.infile)