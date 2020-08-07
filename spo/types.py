from typing import NamedTuple, List


class Chunk(NamedTuple):
    """
    """
    position: int
    spanString: str
    match: str


class Edge(NamedTuple):
    """
    """
    target_text: str
    source_id: int
    deprel: str
    source_text: str


class Sentence(NamedTuple):
    chunks: List[Chunk]
    deps: List[Edge]


class Document(NamedTuple):
    sentences: List[Sentence]

