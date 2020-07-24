import praw
from regex import match
from requests import get
import os
import shutil


red = praw.Reddit(client_id="_4W54SFBNZJwAA",
                  client_secret="jiQj7rsZeozEquzDl9NjudQn-Z8",
                  password="Live-in69",
                  user_agent="testscript by /u/yardley_process",
                  username="yardley_process")

subred = red.subreddit("ImaginarySliceOfLife")

os.mkdir(os.path.join(os.getcwd(), subred.display_name))

for each in subred.hot(limit = 2):
    # print(each.url)

    isImg = match(r".*png|.*jpg*.", each.url)

    # print(isImg)

    if isImg:
        r = get(each.url, stream = True)
        # print(type(r))
        # print(r)
        # print(r.raw)
        if r.status_code == 200:
            r.raw.decode_content = True
            file = open(str(each), "wb")
            shutil.copyfileobj(r.raw, file)
            file.close()

