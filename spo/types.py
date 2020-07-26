from typing import NamedTuple, List


class Chunk(NamedTuple):
    pass


class Dependancy(NamedTuple):
    pass


class Sentence(NamedTuple):
    chunks: List[Chunk]
    deps: List[Dependancy]


class Document(NamedTuple):
    sentences: List[Sentence]

