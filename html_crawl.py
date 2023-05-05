import praw
import json
from bs4 import BeautifulSoup
import requests

list_of_items = []
fields = (#'comments',
          'name',
          'title',
          'url',
          )

comm_fields = ('body')

file_name = f"html_baseball_data.json"


top = reddit.subreddit("baseball").new(limit=1)
for post in top:
    to_dict = vars(post)
    sub_dict = {field:to_dict[field] for field in fields}
    list_of_items.append(sub_dict)
    
    
   
    with open(file_name, "a") as f:
        json.dump(sub_dict, f)
        f.write("\n")
        
    url = post.url
    response = requests.get(url)
    html = response.text
        
    with open(file_name, "a") as f:
        f.write("\n\n")
        json.dump(html, f)
        f.write("\n")
    
print("done")
