( THIS APP IS STILL IN DEVELOPMENT AND WILL NOT WORK )

<img src="https://github.com/tgwaste/TweetKiller/blob/main/icon.png" height=150 width=150>

# TweetKiller
Mass Delete Tweets and Likes from Twitter/X

## Introduction
I was not at all happy with the other cli mass deletion tools. They were aweful so I made this and tried to make it as simple as possible.

## Instructions
- You need to make a developer account.
- You need to make a project and an app with read/write permissions.
- You need to edit auth.json with your keys.
- You need to request and download an archive of your twitter data.
- Example to delete the 10 most recent tweets: ./tweet-killer.py -z your.zip -t -c 10 --confirm
- Example to delete the 10 most recent likes: ./tweet-killer.py -z your.zip -l -c 10 --confirm
- Don't use --confirm if you want to run the script in pretend mode and just view your tweets/likes.
- Just run the script by itself for help.

