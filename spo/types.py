from typing import NamedTuple, List


class Chunk(NamedTuple):
    position: int
    spanString: str
    match: str


class Dep(NamedTuple):
    """
    """
    target_text: str
    source_id: int
    deprel: str
    source_text: str


class Sentence(NamedTuple):
    chunks: List[Chunk]
    deps: List[Dep]


class Document(NamedTuple):
    sentences: List[Sentence]

