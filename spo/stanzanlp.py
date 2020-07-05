import stanza
from stanza.server import CoreNLPClient
from spo.nlp import NLP


class StanzaNLP(NLP):
    """
    class for NLP processor
    """
    # stanza.download('en')  # download English model
    def __init__(self):
        self.nlp = stanza.Pipeline('en')  # initialize English neural pipeline
        self.client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'parse', 'depparse'],
                                    timeout=60000, memory='16G', endpoint='http://localhost:9001')

    def process(self, doc: str):
        doc = self.nlp(doc)  # run annotation over a sentence
        return doc

    def chunk(self, sentence: str):
        ann = self.client.tregex(sentence, 'NP')
        chunks = ann['sentences'][0]  # first sentence
        return chunks
