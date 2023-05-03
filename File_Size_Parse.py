from pprint import pprint
import praw
import os 
import time
from logging.handlers import RotatingFileHandler
import json
import sys



t0 =time.time()
subreddit = reddit.subreddit("sports")
top_posts = subreddit.top(limit=2000)

# convert to dictionary format and save to file
data = []
total_size = 0
prefix = 'sports'
counter = 10
#file_name = prefix + str(counter) + '.json'
file_name = f"reddit_data_{counter}.json"
post_num = 0

for post in top_posts:
    post_num += 1
    print("Post #: ", post_num)
    post_dict = {
        "selftext": post.selftext,
        "title": post.title,
        "id" : post.id,
        "score": post.score,
        "url": post.url,
        "permalink": post.permalink,
        "author": str(post.author),
        "created_utc": post.created_utc,
        
        "post_comments" : str(post.comments.list()),
        #"replies" : str(post.comments.replies)
        #"comment_replies" : str(post.comments.list().replies.list()),
    }
    
    #post.comments.replace_more(limit=None)
    #for comment in post.comments.list():
    #    print(comment.body, file=f)
    #    for reply in comment.replies:
    #        print(reply.body, file=f)
    
    post_size = sys.getsizeof(post_dict)
    #print("Post size: %d" % post_size)
    if total_size + post_size >= 50000:
        counter += 1
        #write_file = prefix + str(counter) + '.json'
        file_name = f"reddit_data_{counter}.json"
        total_size = 0
    
    with open(file_name, "a") as f:
        json.dump(post_dict, f)
        f.write("\n")
    
    #data.append(post_dict)
    total_size += post_size
    print("Total_size: ", total_size)
                     
t1 = time.time()
#print(t1)
t2 = t1 - t0
print("Completed in: ", t2 , "s")
