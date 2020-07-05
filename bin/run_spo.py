import argparse
import os
import csv
from spo.data_reader import DataReader
from spo.nlp import TextProcessor
from spo.utils import get_dependencies, get_triggered, extract_spo
from stanza.server import CoreNLPClient

os.environ['CORENLP_HOME'] = '/Users/jee.hyub.kim/Downloads/stanford-corenlp-4.0.0'
client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
                       timeout=60000, memory='16G', endpoint='http://localhost:9001')


def get_sentence(words):
    s = []
    for w in words:
        s.append(w.text)
    return " ".join(s)


def main():
    dr = DataReader()
    it = dr.get_reader()
    nlp = TextProcessor()

    with open('spos.tsv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')

        for pmcid, title, abstract in list(it):
            doc = nlp.process(abstract)
            for sentence in list(doc.sentences):
                sent = get_sentence(sentence.words)
                trigger = get_triggered(sent)

                if not trigger:
                    continue

                deps = get_dependencies(sentence)
                # chunking
                ann = client.tregex(sent, 'NP')
                chunks = ann['sentences'][0]  # first sentence
                s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
                print("pmcid", pmcid)
                print("sentence", sent)
                print("s: ", s_head)
                print("s: ", s)
                print("p: ", p)
                print("o: ", o_head)
                print("o: ", o)

                print("")
                writer.writerow([pmcid, s_head, s, p, o_head, o, sent])


if __name__ == '__main__':
    main()
