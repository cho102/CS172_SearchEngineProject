from pprint import pprint
import praw
import os 
import time
from logging.handlers import RotatingFileHandler
import json
import sys




t0 =time.time()

top_posts = reddit.subreddit("nfl").new(limit=2000)

# convert to dictionary format and save to file
list_of_items = []
fields = (#'comments',
          'created_utc',
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

total_size = 0
prefix = 'sports'
counter = 0
#file_name = prefix + str(counter) + '.json'
file_name = f"reddit_data_{counter}.json"
post_num = 0

for post in top_posts:
    #post_num += 1
    #print("Post #: ", post_num)
    
    to_dict = vars(post)
    sub_dict = {field:to_dict[field] for field in fields}
    
    comment_size = 0
    reply_size = 0
    
    post.comments.replace_more(limit=None)
    commentsBody = []
    repliesBody = []
    for comment in post.comments.list():
        commentsBody.append(comment.body)
        for reply in comment.replies:
            repliesBody.append(reply.body)
        if repliesBody:
            commentsBody.append(repliesBody)
        repliesBody = []
        
            
    sub_dict["comments"] = commentsBody
    list_of_items.append(sub_dict)
    
    with open(file_name, 'w') as f:
        f.write(" ")
        
    set_path = os.path.join(r"C:\Users\Roz Teves\Desktop\cs172", file_name)
    post_size = os.path.getsize(set_path)
    print("Path is set to %s" % set_path)
    total_size += post_size
    print("File: #", file_name, "      Total_size: ", total_size)
    
    #catch sizer
    if total_size + post_size >= 1000000:
        counter += 1
        file_name = f"reddit_data_{counter}.json"
        total_size = 0
    with open(file_name, 'w') as f:
        for item in list_of_items:
            json.dump(item, f, indent=2)

                     
t1 = time.time()
t2 = t1 - t0
print("Completed in: ", t2 , "s")
