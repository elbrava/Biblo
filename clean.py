from nltk.corpus import stopwords

n = stopwords.words("english")
f = open("people.txt")
people = f.read().split("\n")
f.close()
f = open("places.txt")
places = f.read().split("\n")
f.close()

print(people)
print(places)


def main(f):
    values = f.read().split("\n")
    li_st = []
    _ = [stop(li_st, i) for i in values]
    print(len(values))
    print(len(li_st))
    return li_st


def stop(li_st, val):
    def repeat_remove(li_st, val):
        if not li_st.__contains__(val): li_st.append(val)

    nop = False
    for i in val.split(" "):
        if i in n:
            nop = True
    if not nop:
        repeat_remove(li_st, val)


def place(li_st):
    global places
    for i, v in enumerate(li_st):
        if v in places:
            li_st.remove(li_st[i])
    return li_st


def names(li_st):
    global places
    for i, v in enumerate(li_st):
        if v in people:
            li_st.remove(li_st[i])
    return li_st


print(names(["Adam"]))
with open("nouns.txt", "r") as f:
    nouns = main(f)
    print(nouns)
    print(len(nouns))
    nouns = place(nouns)
    print(len(nouns))
    nouns = names(nouns)
    print(len(nouns))
with open("verbs.txt", "r") as f:
    verbs_main = main(f)
print(nouns)
print(len(verbs_main))

with open("nouns.txt", "w") as f:
    f.write("\n ".join(nouns))
with open("verbs.txt", "w") as f:
    f.write("\n ".join(verbs_main))
