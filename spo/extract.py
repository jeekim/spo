import spo.config as config
from spo.types import Chunk, Edge
from typing import List, Optional
import re


def get_fired_trigger(sentence: str) -> Optional[str]:
    """
    Given a sentence, return a matched triggered, None if no firing.
    :param sentence:
    :return:
    """
    for trigger in config.triggers:
        if re.search(r"\b" + re.escape(trigger) + r"\b", sentence):
            return trigger
    return None


def get_trigger_dep(deps: List[Edge], trigger: str):
    """
    Given a trigger, fetch trigger info: trigger id, edge, source_text (possible head)
    :param deps:
    :param trigger:
    :return:
    """
    # for i, (target_text, source_id, deprel, source_text) in enumerate(deps):
    for i, dep in enumerate(deps):
        if trigger == dep.target_text:
            return i + 1, dep.deprel, dep.source_text
    return None, None, None  # not matched.


def get_s_head(deps: List[Edge], pos: int, edge, source_text) -> str:
    """
    Given dependencies and a trigger info, return a head word of a subject.
    :param deps:
    :param pos:
    :param edge:
    :param source_text:
    :return:
    """
    if edge == "acl:relcl":  # when the trigger is a dependent
        return source_text
    elif edge == 'xcomp':
        # print(source_text)
        p, edge, source = get_trigger_dep(deps, source_text)
        # recursive
        s_head = get_s_head(deps, p, edge, source)
        return s_head
    else:
        pass

    # looking for a dependent of the trigger
    # for target_text, source_id, deprel, _ in deps:
    for dep in deps:
        if int(dep.source_id) == pos and dep.deprel in config.s_dp_list:
            return dep.target_text
    return ''


def get_o_head(deps: List[Edge], pos: int, edge, source_text) -> str:
    for dep in deps:
        if int(dep.source_id) == pos and dep.deprel in config.o_dp_list:
            return dep.target_text
    return ''


def is_np_head(match, head) -> bool:
    """
    Given a constituent and a head, check if the head is the head of the given chunk.
    :param match:
    :param head:
    :return:
    """
    if match.find(f'{head})) (PP (IN') != -1:
        return True
    #  TODO
    elif match.find(f'{head})) (, ,)') != -1 and match.find(f'(PP (IN of)') == -1:
        return True
    elif match.find(f'{head}) (CC and)') != -1:
        return True
    elif match.endswith(f'{head}))'):
        return True
    else:
        return False


def get_longest_np(chunks: List[Chunk], head: str) -> str:
    longest_np = ''
    for chunk in chunks:
        np = chunk.spanString
        match = chunk.match
        match = re.sub(r"\s+", " ", match, flags=re.UNICODE)
        match = match.strip()
        if is_np_head(match, head) and len(np) > len(longest_np):
            longest_np = np
    return longest_np


def get_coordinated_nps(chunk: str) -> List[str]:
    nps = re.split(r"\s*(?:,|but|and)\s+", chunk)
    nps = list(filter(lambda e: len(e) > 0, nps))
    return nps


def extract_spo(deps: List[Edge], chunks: List[Chunk], trigger: str):
    trigger2 = trigger.split(" ")[0]
    p, edge, source = get_trigger_dep(deps, trigger2)
    s_head = get_s_head(deps, p, edge, source)
    o_head = get_o_head(deps, p, edge, source)
    s_np = get_longest_np(chunks, s_head)
    o_np = get_longest_np(chunks, o_head)
    return s_head, s_np, trigger, o_head, o_np

