import argparse
import csv
from spo.data_reader import DataReader
from spo.stanzanlp import StanzaNLP
from spo.extract import get_fired_trigger, extract_spo, get_coordinated_nps


def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input-dir', required=True, help='...')
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
                sent = StanzaNLP.get_sentence(sentence.words)
                trigger = get_fired_trigger(sent)

                if not trigger:
                    continue

                deps = StanzaNLP.get_dependencies(sentence)
                # chunking
                chunks = nlp.prepare_chunks(sent)
                s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
                ss = get_coordinated_nps(s)
                os = get_coordinated_nps(o)

                for s in ss:
                    for o in os:
                        row = [title, pmcid, f'PMC{pmcid}.nxml', s, p, o, sent]
                        if all(row):
                            writer.writerow(row)


if __name__ == '__main__':
    main()
