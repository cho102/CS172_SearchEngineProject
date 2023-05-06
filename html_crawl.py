import praw
import os
import json
import sys
from bs4 import BeautifulSoup
from prawcore import ResponseException
import requests

list_of_items = []
fields = (#'created_utc',
          'id',
          #'name',
          #'num_comments',
          #'over_18',
          #'permalink',
          #'score',
          #'selftext',
          #'spoiler',
          'title',
          #'upvote_ratio',
          'url', 
          #'html_content',
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
    postLimit = None
    print("Number of posts to crawl was set to: " + str(postLimit))

counter = 1
file_name = f"reddit_{subreddit}_{postTypeFilter.lower()}_data_{counter}.json"
with open(file_name, "a") as f:
    f.write("[\n")

reddit = praw.Reddit(client_id=userClientID, client_secret=userClientSecret, user_agent=subreddit + "Scrape", username=redditUsername, password=redditPassword)

if postLimit == None:
    if postTypeFilter.lower() == "top":
        postType = reddit.subreddit(subreddit).top(limit=postLimit)
    elif postTypeFilter.lower() == "hot":
        postType = reddit.subreddit(subreddit).hot(limit=postLimit)
    elif postTypeFilter.lower() == "new":
        postType = reddit.subreddit(subreddit).new(limit=postLimit)
    else:
        print("Failed to crawl, post filter was invalid.")
        quit()
else:
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
    post_cnt = 0
    postHolder = []

    for post in postType:
        post_cnt += 1
        postHolder.append(post)

    currPostCnt = 0
    for post in postHolder:
        currPostCnt += 1
        
        to_dict = vars(post)
        sub_dict = {field:to_dict[field] for field in fields}
        
        url = post.url
        response = requests.get(url)
        html = response.text
        
        soup = BeautifulSoup(html, 'html.parser')
        
        anchors = soup.find_all('a')
        for anchor in anchors:
            href = anchor.get('href')
            if href:
                html_href = {"html_content": href}

        images = soup.find_all('img')
        for image in images:
            src = image.get('src')
            if src:
                html_img = {"html_image": src}
        
        #No elements found
        """elements = soup.find_all('.my-class')
        for element in elements:
            elem = element.get('.my-class')
            if elem:
                html_data = {"html_element": elem}"""
                
        #No headings found        
        """headings = soup.find_all('h1', 'h2', 'h3')
        for heading in headings:
            h = heading.get('h1', 'h2', 'h3')
            if h:
                html_data = {"html_heading": h}"""
        
        #Comments Found
        """post.comments.replace_more(limit=None)
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
        sub_dict["comments"] = commentsBody"""

        list_of_items.append(sub_dict)
        
        with open(file_name, "a") as f:
            json.dump(sub_dict, f)
            f.write(", ")
            json.dump(html_href, f)
            f.write(", ")
            json.dump(html_img, f)
            
            
            
               
        #JSON 10MB Parser
        """if os.path.getsize(file_name) >= 10000000:
          with open(file_name, "a") as f:
            f.write("\n]")
          currentFileSize = round(os.path.getsize(file_name)/(1024*1024), 2)
          print("\n[" + file_name + " reached " + str(currentFileSize) + " MB, creating a new file.]")
          counter += 1
          file_name = f"reddit_{subreddit}_{postTypeFilter.lower()}_data_{counter}.json"
          with open(file_name, "a") as f:
            f.write("[\n")"""
        
        #Post Limiter
        if currPostCnt == post_cnt:
            with open(file_name, 'rb+') as f:
                f.seek(-1, os.SEEK_END)
                f.truncate()
            with open(file_name, "a") as f:
                f.write("}\n]")
                print("Finished crawling r/" + subreddit + ".\n")
                quit()    
        else:
            with open(file_name, "a") as f:
                f.write(",\n")
                
        
        """with open(file_name, "a") as f:
            json.dump(html, f)
            f.write("\n")"""
            
            
print("end of loop, something went wrong")
    
    
