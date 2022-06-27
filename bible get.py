import os

import requests
import bs4


def get_testament():
    pass


def book_split(i, url):
    url = url.split("/")[-2]
    print(url, i)
    if not os.path.exists(f"{i}/{url}/"):
        print("here")
        os.makedirs(r"{}\{}".format(i, url), exist_ok=True)
    get_verses(i, url)
    return url


def get_books():
    r = requests.request("GET", f"https://www.biblestudytools.com/gnt")
    b = bs4.BeautifulSoup(r.content, "lxml")
    b = b.findAll("div", class_="panel-body")
    for i in b:
        books = i.findAll("a")
        books = [book_split(b.index(i) + 1, h["href"]) for h in books]


def get_verses(count, book):
    r = requests.request("GET", f"https://www.biblestudytools.com/gnt/{book}/")
    b = bs4.BeautifulSoup(r.content, "lxml")

    b = b.findAll("div", class_="pull-left")

    for i in b:
        verses = i.find("a")

        try:
            verses = verses["href"]
        except Exception as e:
            pass
        else:
            get_text(count, verses)


def get_text(count, link):
    v = link.split("/")
    print(v)
    r = requests.request("GET", link)
    b = bs4.BeautifulSoup(r.content, "lxml")
    b = b.find("div", class_="scripture verse-padding")
    try:
        b = b.findAll("div", class_="verse font-small")
        print(len(b))
        os.makedirs(f"{count}/{v[-2]}/", exist_ok=True)
        with open(f"{count}/{v[-2]}/{v[-1].split('.html')[0]}.bible", "w") as f:
            f.write("")

        for i in b:
            verses = i.findAll("span")
            # print(verses)
            print(f"{count}/{v[-2]}/{v[-1].split('.html')[0]}.bible")
            with open(f"{count}/{v[-2]}/{v[-1].split('.html')[0]}.bible", "a") as f:
                print(verses[-1].text)
                f.write(verses[-1].text)
                f.write("\n")
                print(verses[-1].text)
    except:
        with open("errors.txt", "a") as f:
            f.write(link)
            f.write("\n")


get_books()