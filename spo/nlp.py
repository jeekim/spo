import stanza
from stanza.server import CoreNLPClient
import os
# import spo.config as config

os.environ['CORENLP_HOME'] = '/Users/jee.hyub.kim/Downloads/stanford-corenlp-4.0.0'


class TextProcessor(object):
    """
    class for NLP processor
    """
    # stanza.download('en')  # download English model
    def __init__(self):
        self.nlp = stanza.Pipeline('en')  # initialize English neural pipeline
        self.client = CoreNLPClient(annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'depparse',
                                                'coref'], timeout=60000, memory='16G', endpoint='http://localhost:9001')

    def process(self, doc: str):
        # if not self._is_fired(text):
        #     return None

        doc = self.nlp(doc)  # run annotation over a sentence
        # s = doc.sentences[0]
        # d = s.to_dict()
        return doc

    def chunk(self, sentence):
        ann = self.client.tregex(sentence, 'NP')
        chunks = ann['sentences'][0]  # first sentence

        return chunks
