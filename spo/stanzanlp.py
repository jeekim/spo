import stanza
from stanza.server import CoreNLPClient
from spo.nlp import NLP
from typing import List

stanza.download('en')


class StanzaNLP(NLP):
    """
    class for NLP processor
    """
    # stanza.download('en')  # download English model
    def __init__(self):
        self.nlp = stanza.Pipeline('en')  # initialize English neural pipeline
        self.client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'parse'],
                                    timeout=60000, memory='4G', endpoint='http://localhost:9001')

    def process(self, doc: str):
        """
        Given an document, outputs annotated documents.
        :param doc:
        :return:
        """
        ann = self.nlp(doc)  # run annotation over a sentence
        return ann

    def chunk(self, doc: str):
        """
        Given a doc, outputs a list of chunks based on phrase structure grammar.
        :param sentence:
        :return:
        """
        ann = self.client.tregex(doc, 'NP')
        # chunks = ann['sentences'][0]  # first sentence
        # return chunks
        return ann

    def prepare_chunks(self, s: str):
        ann = self.chunk(s)
        chunks = ann['sentences'][0]  # first sentence
        return chunks

    def prepare_deps(self, s: str):
        ann = self.process(s)
        sent = ann.sentences[0]
        deps = StanzaNLP.get_dependencies(sent)
        return deps

    @staticmethod
    def get_dependencies(s) -> List:
        deps = []
        for dep_edge in s.dependencies:
            # target text, source id, edge, source text
            deps.append((dep_edge[2].text, dep_edge[0].id, dep_edge[1], dep_edge[0].text))
        return deps

