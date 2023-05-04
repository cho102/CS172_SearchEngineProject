import praw
import json
import os
import sys
from prawcore import ResponseException

list_of_items = []
fields = ('created_utc',
          'id',
          'name',
          'num_comments',
          'over_18',
          'permalink',
          'score',
          'selftext',
          'spoiler',
          'title',
          'upvote_ratio',
          'url', 
          )
comm_fields = ('body')

userClientID = sys.argv[1]
userClientSecret = sys.argv[2]
redditUsername = sys.argv[3]
redditPassword = sys.argv[4]
subreddit = sys.argv[5]
postLimit = sys.argv[6]

if int(postLimit) < 0:
    print("Number of posts to crawl was negative, setting number of posts to crawl to absolute value")
    postLimit = abs(int(postLimit))
    print("Number of posts to crawl was set to: " + str(postLimit))
elif int(postLimit) == 0:
    print("Number of posts to crawl was set 0, setting number of posts to crawl to None")
    postLimit = None
    print("Number of posts to crawl was set to: " + str(postLimit))

counter = 1
file_name = f"reddit_{subreddit}_data_{counter}.json"

reddit = praw.Reddit(client_id=userClientID, client_secret=userClientSecret, user_agent=subreddit + "Scrape", username=redditUsername, password=redditPassword)

if postLimit == None:
    top = reddit.subreddit(subreddit).top(limit=postLimit)
else:
    top = reddit.subreddit(subreddit).top(limit=int(postLimit))

try: # referenced https://stackoverflow.com/a/62110680
    reddit.user.me()
except ResponseException:
    print("\nFailed to crawl, invalid Reddit account credentials and/or app ID/secret inputted")
else:
    print("\nValid Reddit account and app found for user: " + redditUsername)
    print("\nStarting crawling r/" + subreddit + ".")
    for post in top:
        to_dict = vars(post)
        sub_dict = {field:to_dict[field] for field in fields}
        post.comments.replace_more(limit=None)
        commentsBody = []
        for comment in post.comments.list():
            comm_dict = vars(comment)
            comm_sub_dict = {comm_fields:comm_dict[comm_fields] for comm_field in comm_fields}
            repliesBody=[]
            for reply in comment.replies:
                repliesBody.append(reply.body)
            if len(repliesBody):
                comm_sub_dict["replies"] = repliesBody
            commentsBody.append(comm_sub_dict)
        sub_dict["comments"] = commentsBody
        list_of_items.append(sub_dict)
        
        with open(file_name, "a") as f:
            json.dump(sub_dict, f)
            f.write("\n")
        
        if os.path.getsize(file_name) >= 10000000:
            print("\n[Current file reached " + str(round(os.path.getsize(file_name)/(1024*1024)), 2) + " MB, creating a new file.]\n")
            counter += 1
            file_name = f"reddit_{subreddit}_data_{counter}.json"
    #print("\nFile size (in MB): " + str(round(os.path.getsize(file_name)/(1024*1024), 2)))
    print("\nFinished crawling r/" + subreddit + ".")