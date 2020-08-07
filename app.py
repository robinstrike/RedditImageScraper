import praw
import regex
from requests import get
import os
import shutil
import json


def scrape_content(subredditname, count = 25, media = 1):
    subred_object = obtain_subreddit_object(subredditname)
    if media == 1:
        process_images(subred_object, count)
    elif media == 2:
        download_text(subred_object, count)
    elif media == 3:
        download_urls(subred_object, count)


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
        img_filename = extract_file_name(each.url)
        if img_filename is None:
            img_filename = manually_extract_filename(each.url)
        if img_filename:
            download_pics(each, img_filename)


def manually_extract_filename(url):
    if regex.match(r"https://imgur\.com", url):
        modified_url = str(url).replace("imgur", "i.imgur") + ".jpg"
        return extract_file_name(modified_url)
    else:
        return None


def extract_file_name(url):
    img_filename = regex.search(r"[^/\\&\?]+\.(jpeg|jpg|png)(?=([\?&].*$|$))", url)
    if img_filename is not None:
        return img_filename.group(0)
    else:
        return None


def download_pics(each, fname):
    page = get(each.url, stream = True) 
    if page.status_code == 200:
        page.raw.decode_content = True
        file = open(fname, mode = "wb")
        shutil.copyfileobj(page.raw, file)
        file.close()


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

