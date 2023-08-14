# TweetKiller
Mass Delete Tweets and Likes from Twitter/X

## Introduction
I was not at all happy with the other cli mass deletion tools. They were aweful so I made this and tried to make it as simple as possible.

## Instructions
- You need to make a developer account.
- You need to make a project and an app with read/write permissions.
- You need to edit auth.json with your keys.
- You need to request and download an archive of your twitter data.
- Example to delete the 10 most recent tweets: ./tweet-killer.py --zipfile=your.zip --tweets --count 10 --confirm
- Example to delete the 10 most recent likes: ./tweet-killer.py --zipfile=your.zip --likes --count 10 --confirm
- Don't use --confirm if you want to run the script in pretend mode and just view your tweets/likes.

