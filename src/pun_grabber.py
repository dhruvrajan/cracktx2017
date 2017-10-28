# isPun = {}
# with open('../semeval2017_task7/data/test/subtask1-heterographic-test.gold', 'r') as f:
#     for line in f:
#         identifier, label = tuple(line.strip().split())
#         isPun[identifier] = False if (label == '0') else True

import xml.etree.ElementTree as ET
import pickle
import random
from collections import defaultdict
from nltk.corpus import wordnet as wn
import networkx as nx

def closure_graph(synset, fn):
    seen = set()
    graph = nx.DiGraph()

    def recurse(s):
        if not s in seen:
            seen.add(s)
            graph.add_node(s.name)
            for s1 in fn(s):
                graph.add_node(s1.name)
                graph.add_edge(s.name, s1.name)
                recurse(s1)

    recurse(synset)
    return seen


def extract_puns(pun_files):
    puns = defaultdict(lambda: None)

    for pun_file in pun_files:
        tree = ET.parse(pun_file)
        root = tree.getroot()

        for child in root:
            punID = child.attrib["id"]
            pun = []
            for subchild in child:
                pun.append(subchild.text)
            puns[punID] = pun

    return dict(puns)


def create_inverted_index(puns, mapping_files):
    inverted_index = defaultdict(lambda: None)
    for mapping_file in mapping_files:
        with open(mapping_file, 'r') as f:
            for line in f:
                punID, word = tuple(line.strip().split())
                wordID = int(word.split("_")[-1]) - 1
                the_word = puns[punID][wordID]
                if not inverted_index[the_word]:
                    punIDList = []
                    punIDList.append(punID)
                    inverted_index[the_word] = punIDList
                else:
                    inverted_index[the_word].append(punID)

    return dict(inverted_index)


def load_data():
    with open("inverted_index.idx", "rb") as f:
        inverted_index, puns = pickle.load(f)

    return inverted_index, puns


def generate_pun(phrase):
    inverted_index, puns = load_data()
    for word in phrase:
        try:
            pun_ids = inverted_index[word]
            return puns[random.choice(pun_ids)]
        except:
            pass

    return None


def main():
    puns = extract_puns(['../semeval2017_task7/data/test/subtask2-heterographic-test.xml',
                     '../semeval2017_task7/data/test/subtask2-homographic-test.xml'])
    inverted_index = create_inverted_index(puns, ['../semeval2017_task7/data/test/subtask2-heterographic-test.gold',
                                                 '../semeval2017_task7/data/test/subtask2-homographic-test.gold'])

    with open("inverted_index.idx", "wb") as f:
        pickle.dump((inverted_index, dict(puns)), f)

    with open("inverted_index.idx", "rb") as f:
        inverted_index, puns = pickle.load(f)

    print(inverted_index["alleged"])
    print(puns[inverted_index["alleged"][0]])
    print(inverted_index["vault"])
    print(generate_pun(["bovine"]))
    dog = wn.synset('dog.n.01')
    setx = closure_graph(dog,
                      lambda s: s.hypernyms())
    print(setx)


if __name__ == "__main__":
    main()
