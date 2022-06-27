import bs4
import requests

j = []
r = requests.request("GET", "https://en.wikipedia.org/wiki/List_of_biblical_places")
b = bs4.BeautifulSoup(r.content, "lxml")
h = [str(i.text) for i in b.findAll("a")]
print("\n".join(h[0:-50]))
with open("places.txt", "w") as f:
    f.write("\n".join(h[17:-50]))
