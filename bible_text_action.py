import os

import nltk
import pandas as pd
import youtubesearchpython
from nltk import Tree

place = "Eden"
time = "4000 BC"
bible_verse_counter = 0
name = "God"

nouns = []
verbs_main = []
sentences = []


class Action():
    def __init__(self, sentence, bible_verse):
        global place
        global time
        global name
        global bible_verse_counter
        sentences.append(sentence)
        verbs = [i[0] for i in nltk.pos_tag(nltk.word_tokenize(sentence)) if
                 i[1] == "VB" or i[1] == "VBD" or i[1] == "VBG" or i[1] == "VBN" or i[1] == "VBP" or i[1] == "VBZ"]
        verbs_main.extend(verbs)
        if verbs:

            self.subjects = [i[0] for i in nltk.pos_tag(nltk.word_tokenize(sentence)[:sentence.index(verbs[0]) - 1]) if
                             i[1] == "NN" or i[1] == "NNP" or i[1] == "NNPS" or i[1] == "NNS" or i[1] == "PRP"]
            self.objects = [i[0] for i in nltk.pos_tag(nltk.word_tokenize(sentence)[sentence.index(verbs[-1]):-1]) if
                            i[1] == "NN" or i[1] == "NNP" or i[1] == "NNPS" or i[1] == "NNS" or i[1] == "PRP"]

            self.actions = verbs
            grammar = r"""
            NP: { < DT | JJ | NN. * > +}  # Chunk sequences of DT, JJ, NN
            PP: { < IN > < NP >}  # Chunk prepositions followed by NP
            VP: { < VB. * > < NP | PP | CLAUSE > +$}  # Chunk verbs and their arguments
            CLAUSE: { < NP > < VP >}
            """
            self.how = ""
            for i in nltk.RegexpParser(grammar).parse(nltk.pos_tag(nltk.word_tokenize(sentence))):
                if type(i) == Tree:
                    if i._label == "PP":
                        print("node")
                        print(i.pretty_print())
                        print(i.leaves())
                        self.how = " ".join([o[0] for o in i.leaves()])

            # action with time
            print(self.how)
            self.why = ""

            self.bible_verse = bible_verse
            # found not to be neccessary
            places_file = open("places.txt", "r")
            name_file = open("people.txt", "r")
            for word in self.objects + self.subjects:
                if places_file.read().split("/n").__contains__(word):
                    place = word
                if name_file.read().split("/n").__contains__(word):
                    name = word
                nouns.append(word)

            self.where = place
            self.when = time
            self.who = name

    def search(self):
        pass
        # youtubesearchpython.search()
        # search for of  it online


def main():
    for i in os.listdir("1"):
        print(i)
        for o in os.listdir("1/" + i):
            with open("1/" + i + f"/{o}") as f:
                # print("1/" + i + f"/{o}")
                # print(nltk.sent_tokenize(f.read()))

                # n in nltk.sent_tokenize(f.read()):
                s = str(o).split(".bible")[0]
                print(f"{i} {s} ")
                a = Action(f"{nltk.sent_tokenize(f.read())[0]}", s)
    for i in os.listdir("2"):
        print(i)
        for o in os.listdir("2/" + i):
            with open("2/" + i + f"/{o}") as f:
                # print("1/" + i + f"/{o}")
                # print(nltk.sent_tokenize(f.read()))

                # n in nltk.sent_tokenize(f.read()):
                s = str(o).split(".bible")[0]
                print(f"{i} {s} ")
                a = Action(f"{nltk.sent_tokenize(f.read())[0]}", s)
    with open("sentences.txt", "w") as f:
        f.write("\n ".join(sentences))
    with open("nouns.txt", "w") as f:
        f.write("\n ".join(nouns))
    with open("verbs.txt", "w") as f:
        f.write("\n ".join(verbs_main))


main()
"""
To save some folks some time, here is a list I extracted from a small corpus. I do not know if it is complete, but it should have most (if not all) of the help definitions from upenn_tagset...

CC: conjunction, coordinating

& 'n and both but either et for less minus neither nor or plus so
therefore times v. versus vs. whether yet
CD: numeral, cardinal

mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
fifteen 271,124 dozen quintillion DM2,000 ...
DT: determiner

all an another any both del each either every half la many much nary
neither no some such that the them these this those
EX: existential there

there
IN: preposition or conjunction, subordinating

astride among upon whether out inside pro despite on by throughout
below within for towards near behind atop around if like until below
next into if beside ...
JJ: adjective or numeral, ordinal

third ill-mannered pre-war regrettable oiled calamitous first separable
ectoplasmic battery-powered participatory fourth still-to-be-named
multilingual multi-disciplinary ...
JJR: adjective, comparative

bleaker braver breezier briefer brighter brisker broader bumper busier
calmer cheaper choosier cleaner clearer closer colder commoner costlier
cozier creamier crunchier cuter ...
JJS: adjective, superlative

calmest cheapest choicest classiest cleanest clearest closest commonest
corniest costliest crassest creepiest crudest cutest darkest deadliest
dearest deepest densest dinkiest ...
LS: list item marker

A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005
SP-44007 Second Third Three Two * a b c d first five four one six three
two
MD: modal auxiliary

can cannot could couldn't dare may might must need ought shall should
shouldn't will would
NN: noun, common, singular or mass

common-carrier cabbage knuckle-duster Casino afghan shed thermostat
investment slide humour falloff slick wind hyena override subhumanity
machinist ...
NNP: noun, proper, singular

Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
Shannon A.K.C. Meltex Liverpool ...
NNS: noun, common, plural

undergraduates scotches bric-a-brac products bodyguards facets coasts
divestitures storehouses designs clubs fragrances averages
subjectivists apprehensions muses factory-jobs ...
PDT: pre-determiner

all both half many quite such sure this
POS: genitive marker

' 's
PRP: pronoun, personal

hers herself him himself hisself it itself me myself one oneself ours
ourselves ownself self she thee theirs them themselves they thou thy us
PRP$: pronoun, possessive

her his mine my our ours their thy your
RB: adverb

occasionally unabatingly maddeningly adventurously professedly
stirringly prominently technologically magisterially predominately
swiftly fiscally pitilessly ...
RBR: adverb, comparative

further gloomier grander graver greater grimmer harder harsher
healthier heavier higher however larger later leaner lengthier less-
perfectly lesser lonelier longer louder lower more ...
RBS: adverb, superlative

best biggest bluntest earliest farthest first furthest hardest
heartiest highest largest least less most nearest second tightest worst
RP: particle

aboard about across along apart around aside at away back before behind
by crop down ever fast for forth from go high i.e. in into just later
low more off on open out over per pie raising start teeth that through
under unto up up-pp upon whole with you
TO: "to" as preposition or infinitive marker

to
UH: interjection

Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen
huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly
man baby diddle hush sonuvabitch ...
verb, present tense, 3rd person singular

bases reconstructs marks mixes displeases seals carps weaves snatches
slumps stretches authorizes smolders pictures emerges stockpiles
seduces fizzes uses bolsters slaps speaks pleads ..."""
"""
place
name
person
time
how preposition
search for specific action media is easy


"""
