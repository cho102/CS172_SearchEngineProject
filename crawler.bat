@echo off
echo Batch Script to take input.
set /p "userClientID=Enter Reddit script app client ID: "
set /p "userClientSecret=Enter Reddit script app client secret: "
set /p "subreddit=Enter subreddit name to crawl: "
set /p "postLimit=Enter the number of posts to crawl: "

cls

echo Client ID is: %userClientID%
echo Client Secret is: %userClientSecret%
echo Subreddit is: %subreddit%
echo Post limit is: %postLimit%
python praw_reddit_crawler_cs172.py %userClientID% %userClientSecret% %subreddit% %postLimit%
pause