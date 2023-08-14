#!/usr/bin/python3 -B

import json, optparse, os, requests_oauthlib, sys, time, zipfile

parser = optparse.OptionParser(usage='usage: %prog [options]')
parser.add_option('-a', '--auth', dest='auth', type='string', default='auth.json', help='path to auth file')
parser.add_option('-c', '--count', dest='count', type='int', default=0, help='how many to delete')
parser.add_option('-l', '--likes', dest='likes', action='store_true', default=False, help='delete likes')
parser.add_option('-t', '--tweets', dest='tweets', action='store_true', default=False, help='delete tweets')
parser.add_option('-z', '--zipfile', dest='zipfile', type='string', default='archive.zip', help='path to twitter zip file')
parser.add_option('-C', '--confirm', dest='confirm', action='store_true', default=False, help='really delete')
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
twitter_user_id = json.loads(response.text)['id_str']

print('API OAuth Token: %s' % (resource_owner_key))
print('Twitter User ID: %s' % (twitter_user_id))

def extract(src, dst, force=False):
	if os.path.exists(dst) and force is False:
		return
	with zipfile.ZipFile(options.zipfile, 'r') as z:
		zipdata = str(z.read(src).decode("utf-8"))
		while zipdata[0] != '[': zipdata = zipdata[1:]
	with open(dst, 'w') as f:
		f.write(zipdata)
	with open(dst, 'r') as f:
		lines = sum(1 for _ in f)
	print('Extracted: %s (%d lines)' % (dst, lines))

extract('data/tweets.js', '/tmp/tweets.json', True)
extract('data/like.js', '/tmp/likes.json', True)

def oauth_get(url):
	response = oauth.get(url)
	if response.status_code != 200:
		print('\nRequest returned an error: {} {}'.format(response.status_code, json.dumps(json.loads(response.text), sort_keys = False, indent = 4)))
		sys.exit(1)
	return json.loads(response.text)

jsondata = oauth_get('https://api.twitter.com/2/users/:'+twitter_user_id+'/liked_tweets')
print(json.dumps(jsondata, sort_keys=False, indent=4))
