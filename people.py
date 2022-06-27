import bs4
import requests

r = requests.request("GET", "https://www.behindthename.com/names/usage/biblical")
b = bs4.BeautifulSoup(r.content, "lxml")
l = [str(i.text).split(" ")[0] for i in b.findAll("a", class_="nll")]
print(l)
r = requests.request("GET", "https://www.behindthename.com/names/usage/biblical/2")
b = bs4.BeautifulSoup(r.content, "lxml")
l += [str(i.text).split(" ")[0] for i in b.findAll("a", class_="nll")]
print(l)
f = open("people.txt", "w")
f.write("\n".join(l))
f.close()
