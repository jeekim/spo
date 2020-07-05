import stanza
from stanza.server import CoreNLPClient
from spo.nlp import NLP

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
        doc = self.nlp(doc)  # run annotation over a sentence
        return doc

    def chunk(self, sentence: str):
        """
        Given a sentence, outputs a list of chunks based on phrase structure grammar.
        :param sentence:
        :return:
        """
        ann = self.client.tregex(sentence, 'NP')
        chunks = ann['sentences'][0]  # first sentence
        return chunks
