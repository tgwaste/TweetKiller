#!/usr/bin/python3 -B

import json, optparse, os, requests_oauthlib, sys, time, zipfile

# some colors
GA = '\033[1;30m'
RE = '\033[1;31m'
GR = '\033[1;32m'
PI = '\033[1;35m'
NC = '\033[0m'

parser = optparse.OptionParser(usage='usage: %prog [options]')
parser.add_option('-a', '--auth', dest='auth', type='string', default='auth.json', help='path to auth file')
parser.add_option('-c', '--count', dest='count', type='int', default=0, help='how many to delete')
parser.add_option('-d', '--delete', dest='delete', action='store_true', default=False, help='really delete')
parser.add_option('-f', '--force', dest='force', action='store_true', default=False, help='force re-create json files')
parser.add_option('-l', '--likes', dest='likes', action='store_true', default=False, help='delete likes')
parser.add_option('-t', '--tweets', dest='tweets', action='store_true', default=False, help='delete tweets')
parser.add_option('-z', '--zipfile', dest='zipfile', type='string', default='archive.zip', help='path to twitter zip file')
(options, args) = parser.parse_args()

if len(sys.argv[1:]) == 0:
	parser.print_help()
	sys.exit(1)

with open(options.auth, 'r') as f:
	credentials = json.load(f)

request_token_url = 'https://api.twitter.com/oauth/request_token'
oauth = requests_oauthlib.OAuth1Session(credentials['consumer_key'], client_secret=credentials['consumer_secret'])

try:
	fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
	print('Unable to Authenticate, there may been an issue with your consumer_key or consumer_secret.')

resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

oauth = requests_oauthlib.OAuth1Session(
	credentials['consumer_key'],
	client_secret=credentials['consumer_secret'],
	resource_owner_key=credentials['access_token'],
	resource_owner_secret=credentials['access_token_secret'],
)

response = oauth.get('https://api.twitter.com/1.1/account/verify_credentials.json')
jsondata = json.loads(response.text)
twitter_user_id = jsondata['id_str']
twitter_screen_name = jsondata['screen_name']

print('API OAuth Token: %s' % (resource_owner_key))
print('Twitter User ID: %s%s%s (%s)' % (PI, twitter_screen_name, NC, twitter_user_id))

if options.delete is False:
	print(GR + 'SAFE MODE' + NC)

def extract(src, dst, force=False):
	if os.path.exists(dst) and force is False:
		return
	with zipfile.ZipFile(options.zipfile, 'r') as z:
		zipdata = str(z.read(src).decode('utf-8'))
		while zipdata[0] != '[': zipdata = zipdata[1:]
	with open(dst, 'w') as f:
		f.write(zipdata)
	with open(dst, 'r') as f:
		lines = sum(1 for _ in f)
	print('Created: %s (%d lines)' % (dst, lines))

def scrub(json_file, thelist, deleted):
	thelist = thelist[deleted:]
	with open(json_file, 'w') as f:
		f.write(json.dumps(thelist, sort_keys=False, indent=4))

tweets_file = '/tmp/tweets.json'
likes_file = '/tmp/likes.json'

extract('data/tweets.js', tweets_file, options.force)
extract('data/like.js', likes_file, options.force)

if options.tweets:
	deleted = 0
	with open(tweets_file, 'r') as f:
		tweets = json.load(f)
	print()
	if len(tweets) < 1:
		print('nothing to delete, %s is empty' % (tweets_file))
	for tweet in tweets:
		print('Tweet: '+ tweet['tweet']['full_text'])
		print(tweet['tweet']['retweet_count'] + ' Retweets || ' + tweet['tweet']['favorite_count'] + " Likes || Date: " + tweet['tweet']['created_at'])
		if options.delete:
			response = oauth.delete('https://api.twitter.com/2/tweets/:'+tweet['tweet']['id'])
			if response.status_code == 200:
				deleted += 1
				print('Tweet DELETED (%d)' % (response.status_code))
			else:
				print('\nRequest returned an error: [{}] {}'.format(response.status_code, json.dumps(json.loads(response.text), sort_keys = False, indent = 4)))
				sys.exit(1)
		print()
		options.count -= 1
		if options.count < 1:
			break
	scrub(tweets_file, tweets, deleted)
	print()
	print('%d total || %d deleted' % (len(tweets)-deleted, deleted))

if options.likes:
	deleted = 0
	with open(likes_file, 'r') as f:
		likes = json.load(f)
	print()
	if len(likes) < 1:
		print('nothing to delete, %s is empty' % (likes_file))
	for like in likes:
		if 'fullText' not in like['like']:
			deleted += 1
			continue
		print('Like: ' + like['like']['fullText'])
		print('Tweet ID: ' + like['like']['tweetId'])
		if options.delete:
			response = oauth.delete('https://api.twitter.com/2/users/:'+twitter_user_id+'/likes/:'+like['like']['tweetId'])
			if response.status_code == 200:
				print('Like DELETED (%d)' % (response.status_code))
				deleted += 1
			else:
				print('\nRequest returned an error: [{}] {}'.format(response.status_code, json.dumps(json.loads(response.text), sort_keys = False, indent = 4)))
				sys.exit(1)
		print()
		options.count -= 1
		if options.count < 1:
			break
	scrub(likes_file, likes, deleted)
	print()
	print('%d total || %d deleted' % (len(likes)-deleted, deleted))
