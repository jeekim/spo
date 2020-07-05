import abc


class NLP(abc.ABC):
    @abc.abstractmethod
    def process(self, doc):
        raise NotImplementedError

    @abc.abstractmethod
    def chunk(self, sentence):
        raise NotImplementedError
