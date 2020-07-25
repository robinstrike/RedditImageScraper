import praw
from regex import match
from requests import get
import os
import shutil


def scrapeimgs(subredditname, count):
    red = praw.Reddit(client_id="_4W54SFBNZJwAA",
                      client_secret="jiQj7rsZeozEquzDl9NjudQn-Z8",
                      password="Live-in69",
                      user_agent="testscript by /u/yardley_process",
                      username="yardley_process")

    subRed = red.subreddit(subredditname)

    os.mkdir(os.path.join(os.getcwd(), subRed.display_name))

    for each in subRed.hot(limit = count):

        isImg = match(r".*\.png.*|.*\.jpg.*", each.url)

        if isImg is None:
            if match(r"https://imgur\.com", each.url):
                each.url = str(each.url).replace("imgur", "i.imgur") + ".jpg"
                isImg = True
                

        if isImg:
            r = get(each.url, stream = True)
            if r.status_code == 200:
                r.raw.decode_content = True
                file = open(os.path.join(os.getcwd(), 
                                         subRed.display_name, str(each) + ".jpg"), "wb")
                shutil.copyfileobj(r.raw, file)
                file.close()

