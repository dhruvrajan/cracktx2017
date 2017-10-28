# isPun = {}
# with open('../semeval2017_task7/data/test/subtask1-heterographic-test.gold', 'r') as f:
#     for line in f:
#         identifier, label = tuple(line.strip().split())
#         isPun[identifier] = False if (label == '0') else True

import xml.etree.ElementTree as ET
import pickle
from collections import defaultdict

tree = ET.parse('../semeval2017_task7/data/test/subtask2-heterographic-test.xml')
root = tree.getroot()

puns = defaultdict(lambda: None)

for child in root:
    punID = child.attrib["id"]
    pun = []
    for subchild in child:
        pun.append(subchild.text)
    puns[punID] = pun


invertedIndex = defaultdict(lambda: None)

with open('../semeval2017_task7/data/test/subtask2-heterographic-test.gold', 'r') as f:
    for line in f:
        punID, word = tuple(line.strip().split())
        wordID = int(word.split("_")[-1]) - 1
        the_word = puns[punID][wordID]
        if not invertedIndex[the_word]:
            punIDList = []
            punIDList.append(punID)
            invertedIndex[the_word] = punIDList
        else:
            invertedIndex[the_word].append(punID)

invertedIndex = dict(invertedIndex)

with open("inverted_index.idx", "wb") as f:
    pickle.dump((invertedIndex, dict(puns)), f)

with open("inverted_index.idx", "rb") as f:
    inv_index, puns_ = pickle.load(f)

print(inv_index["alleged"])
print(puns_[inv_index["alleged"][0]])
