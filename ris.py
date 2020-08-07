import app

"""
app.scrape_content("subreddit", count, media)

subreddit : name of subreddit
count : number of posts to grab (default = 25)
media : 1 for pics (default)
media : 2 for text
media : 3 for urls
"""

app.scrape_content(subredditname = "writingprompts", count = 10, media = 2)

