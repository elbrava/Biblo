import cv2
import pafy
from youtubesearchpython import VideosSearch


def get_youtube_url(query):
    videosSearch = VideosSearch(query, limit=1)
    links = []
    d = videosSearch.result()["result"]
    for i in d:
        links.append(i["link"])

    return links
def main():

    with open("verbs.txt", "r") as f:
        que = f.read().split("\n")
        for i in que:
            p = pafy.new(get_youtube_url(i)[0])
            print(i)
            best = p.getbest(preftype="mp4")
            webcam = cv2.VideoCapture(best.url)
            print(best.url)
            while webcam.isOpened():
                sucess, frame = webcam.read()
                try:
                    cv2.imshow("hh", frame)
                    cv2.waitKey(1)
                except:
                    break
