import praw
import os
import json
import sys
from bs4 import BeautifulSoup
from prawcore import ResponseException

post_cnt = 0

list_of_items = []
fields = ('created_utc',
          )
comm_fields = ('body')

userClientID = sys.argv[1]
userClientSecret = sys.argv[2]
redditUsername = sys.argv[3]
redditPassword = sys.argv[4]
subreddit = sys.argv[5]
postLimit = sys.argv[6]
postTypeFilter = sys.argv[7]

if int(postLimit) < 0:
    print("Number of posts to crawl was negative, setting number of posts to crawl to absolute value")
    postLimit = abs(int(postLimit))
    print("Number of posts to crawl was set to: " + str(postLimit))
elif int(postLimit) == 0:
    print("Number of posts to crawl was set 0, setting number of posts to crawl to None")
    postLimit = 2147483647
    print("Number of posts to crawl was set to: " + str(postLimit))

counter = 1
file_name = f"reddit_{subreddit}_{postTypeFilter.lower()}_data_{counter}.json"
with open(file_name, "a") as f:
    f.write("[\n")


reddit = praw.Reddit(client_id=userClientID, client_secret=userClientSecret, user_agent=subreddit + "Scrape", username=redditUsername, password=redditPassword)

"""if postLimit == None:
    if postTypeFilter.lower() == "top":
        postType = reddit.subreddit(subreddit).top(limit=postLimit)
    elif postTypeFilter.lower() == "hot":
        postType = reddit.subreddit(subreddit).hot(limit=postLimit)
    elif postTypeFilter.lower() == "new":
        postType = reddit.subreddit(subreddit).new(limit=postLimit)
    else:
        print("Failed to crawl, post filter was invalid.")
        quit()
else:"""
if postTypeFilter.lower() == "top":
    postType = reddit.subreddit(subreddit).top(limit=int(postLimit))
elif postTypeFilter.lower() == "hot":
    postType = reddit.subreddit(subreddit).hot(limit=int(postLimit))
elif postTypeFilter.lower() == "new":
    postType = reddit.subreddit(subreddit).new(limit=int(postLimit))
else:
    print("Failed to crawl, post filter was invalid.")
    quit()

try: # referenced https://stackoverflow.com/a/62110680
    reddit.user.me()
except ResponseException:
    print("\nFailed to crawl, invalid Reddit account credentials and/or app ID/secret inputted")
else:
    print("\nValid Reddit account and app found for user: " + redditUsername)
    print("\nStarting crawling r/" + subreddit + ".")
    for post in postType:
        post_cnt += 1
        print("post #", post_cnt)
        to_dict = vars(post)
        sub_dict = {field:to_dict[field] for field in fields}
        #post.comments.replace_more(limit=None)
        """commentsBody = []
        for comment in post.comments.list():
            comm_dict = vars(comment)
            comm_sub_dict = {comm_fields:comm_dict[comm_fields] for comm_field in comm_fields}
            repliesBody=[]
            for reply in comment.replies:
                repliesBody.append(reply.body)
            if len(repliesBody):
                comm_sub_dict["replies"] = repliesBody
            commentsBody.append(comm_sub_dict)
        sub_dict["comments"] = commentsBody"""
        list_of_items.append(sub_dict)
        
        with open(file_name, "a") as f:
            json.dump(sub_dict, f)
            #f.write("\n")
        
        if os.path.getsize(file_name) >= 10000000:
          with open(file_name, "a") as f:
            f.write("\n]")
          currentFileSize = round(os.path.getsize(file_name)/(1024*1024), 2)
          print("\n[" + file_name + " reached " + str(currentFileSize) + " MB, creating a new file.]")
          counter += 1
          file_name = f"reddit_{subreddit}_{postTypeFilter.lower()}_data_{counter}.json"
          with open(file_name, "a") as f:
            f.write("[\n")
        
            
        
        if post_cnt == int(postLimit):
            with open(file_name, 'rb+') as f:
                f.seek(-1, os.SEEK_END)
                f.truncate()
                print("limit reached")
        
            
        else:
            with open(file_name, "a") as f:
                f.write(",\n")
            
        
        
    #print("\nFile size (in MB): " + str(round(os.path.getsize(file_name)/(1024*1024), 2)))
    print("Finished crawling r/" + subreddit + ".\n")
    
    
