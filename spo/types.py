from typing import NamedTuple, List


class Chunk(NamedTuple):
    position: int
    spanString: str
    match: str


class Dependancy(NamedTuple):
    pass


class Sentence(NamedTuple):
    chunks: List[Chunk]
    deps: List[Dependancy]


class Document(NamedTuple):
    sentences: List[Sentence]

