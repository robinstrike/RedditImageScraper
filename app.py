import praw
import regex
from requests import get
import os
import shutil
import json
from bs4 import BeautifulSoup


def scrape_content(subredditname, count, media):
    subred_object = obtain_subreddit_object(subredditname)
    if media == 1:
        process_images(subred_object, count)
    elif media == 2:
        download_text(subred_object, count)
    elif media == 3:
        download_urls(subred_object, count)
    elif media == 4:
        download_gifs(subred_object, count)


def obtain_subreddit_object(subredditname):
    red_object = praw.Reddit(client_id = "xxxx",
                             client_secret = "xxxx",
                             password = "xxxx",
                             user_agent = "xxxx",
                             username = "xxxx")
    subred_object = red_object.subreddit(subredditname)
    return subred_object


def process_images(sro, count):
    make_dir(sro, "_pics")
    for each in sro.hot(limit = count):
        if each.stickied:
            continue
        download_pics(each.url)


def manually_extract_filename(url):
    if regex.match(r"https://imgur\.com", url):
        modified_url = str(url).replace("imgur", "i.imgur") + ".jpg"
        return extract_file_name(modified_url)
    else:
        return None


def extract_file_name(url):
    img_filename = regex.search(r"[^/\\&\?]+\.(jpeg|jpg|png|gif|mp4|webm)(?=([\?&].*$|$))", url)
    if img_filename is not None:
        return img_filename.group(0)
    else:
        return manually_extract_filename(url)


def download_pics(url):
    fname = extract_file_name(url)
    try:
        page = get(url, stream = True)
    except:
        return
    if page.status_code == 200:
        page.raw.decode_content = True
        file = open(fname, mode = "wb")
        try:
            shutil.copyfileobj(page.raw, file)
        except:
            return
        file.close()


def download_gifs(sro, count):
    make_dir(sro, "_gifs")
    for each in sro.hot(limit = count):
        if each.stickied:
            continue
        if regex.match(r".*\.png|.*\.jpg", each.url):
            continue
        if regex.match(r".*\.gif$", each.url):
            download_pics(each.url)
            continue
        page = get(each.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        if regex.match(r".*redgifs", each.url):
            try:
                c_url = soup.find("video").find("source")['src']
            except:
                continue
            if regex.match(r".*thcf(?=6|8|3).", c_url):
                download_pics(c_url)
        elif regex.match(r".*gfycat", each.url):
            if soup.find("title").string == "Page not found | Gfycat":
                continue
            try:
                c_url = soup.find("video").find("source")['src']
            except:
                continue
            if regex.match(r"https:\/\/thcf", c_url):
                if not regex.match(r".*thcf(?=6|8|3).", c_url):
                    continue
            download_pics(c_url)
        elif regex.match(r".*imgur", each.url):
            try:
                c_url = "https:" + soup.find("source")['src']
            except:
                continue
            download_pics(c_url)
        else:
            continue


def download_text(sro, count):
    make_dir(sro, "_text")
    f = sro.display_name + "_text.txt"
    file = open(f, mode = "a")
    for each in sro.hot(limit = count):
        if each.stickied:
            continue
        file.write(each.title + "\n")
        file.write(each.selftext + "\n" + "\n" + "\n")
    file.close()


def download_urls(sro, count):
    make_dir(sro, "_urls")
    fname = sro.display_name + "_urls.json"
    create_jsonfile(fname)
    with open(fname) as f:
        data = json.load(f)
        temp = data['urls']
        for each in sro.hot(limit = count):
            if each.stickied:
                continue
            post = {"title": each.title, "text": each.selftext, "url": each.url}
            temp.append(post)

    with open(fname, 'w') as f:     # opening in write mode to rewrite
        json.dump(data, f, indent = 4)


def make_dir(sro, type):
    path, folder = os.path.split(os.getcwd())
    new_folder = str(sro) + type
    new_path = os.path.join(path, new_folder)
    i = 1
    while os.path.exists(new_path):
        new_path = new_path + str(i)
    os.mkdir(new_path)
    os.chdir(new_path)


def create_jsonfile(fname):
    with open(fname, mode = 'w') as f:
        f.write("{\"urls\":[]}")


# utility methods
def get_urls(sro, count):
    sro = obtain_subreddit_object(sro)
    for each in sro.hot(limit = count):
        with open("new_f.txt", mode = "a") as f:
            f.write(each.url + "\n")


def count_origin(subredname, count):
    sro = obtain_subreddit_object(subredname)
    f = open("u.txt", "a")

    r = 0
    g = 0
    i = 0
    o = 0
    red = 0

    for each in sro.hot(limit = count):
        s = str(each.url)
        f.write(s + "\n")
        if regex.match(r".*redgifs.*", s):
            r = r+1
        elif regex.match(r".*gfycat.*", s):
            g = g+1
        elif regex.match(r".*imgur.*", s):
            i = i+1
        elif regex.match(r".*redd.*", s):
            red = red+1
        else:
            o = o + 1
    f.close()
    print("redgifs = " + str(r) + "\n" + "gfycat = " + str(g) + "\n" + "imgur = " + str(i) + "\n" + "reddit = " + str(red) + "\n" + "others = " + str(o) + "\n")

