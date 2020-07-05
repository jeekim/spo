import argparse
import csv
import spo.config as config
from spo.data_reader import DataReader
from spo.stanzanlp import StanzaNLP
from spo.utils import get_dependencies, get_fired_trigger, extract_spo
from stanza.server import CoreNLPClient

# client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse', 'coref'],
client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'parse', 'depparse'],
                       timeout=60000, memory='16G', endpoint='http://localhost:9001')


def get_sentence(words):
    s = []
    for w in words:
        s.append(w.text)
    return " ".join(s)


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input-dir', required=False, default=config.DATA_DIR, help='...')
    parser.add_argument('-o', '--output-file', required=True, help='...')

    args = parser.parse_args()

    dr = DataReader(args.input_dir)
    it = dr.get_reader()
    nlp = StanzaNLP()

    with open(args.output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')

        for pmcid, title, abstract in list(it):
            doc = nlp.process(abstract)
            for sentence in list(doc.sentences):
                sent = get_sentence(sentence.words)
                trigger = get_fired_trigger(sent)

                if not trigger:
                    continue

                deps = get_dependencies(sentence)
                # chunking
                ann = client.tregex(sent, 'NP')
                chunks = ann['sentences'][0]  # first sentence
                s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
                # print("pmcid", pmcid)
                # print("sentence", sent)
                # print("s: ", s_head)
                # print("s: ", s)
                # print("p: ", p)
                # print("o: ", o_head)
                # print("o: ", o)
                # print("")
                row = [pmcid, s, p, o, sent]
                if all(row):
                    writer.writerow(row)


if __name__ == '__main__':
    main()
