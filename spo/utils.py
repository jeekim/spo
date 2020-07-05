import spo.config as config
from typing import List, Optional
import re


def get_dependencies(s) -> List:
    deps = []
    for dep_edge in s.dependencies:
        deps.append((dep_edge[2].text, dep_edge[0].id, dep_edge[1], dep_edge[0].text))
    return deps


def get_triggered(sentence: str) -> Optional[str]:
    for trigger in config.triggers:
        # if sentence.find(trigger) != -1:
        if sentence.find(trigger) != -1:
            return trigger # .split(" ")[0]
    return None


def get_trigger(deps: List, trigger: str):
    for i, (text, id, edge, head) in enumerate(deps):
        if trigger == text:
            return i + 1, edge, head
    return None, None, None  # not matched.


# TODO _acl:relcl
def get_s_head(deps: List, pos: int, edge, source) -> str:
    text = ''
    if edge == "acl:relcl":
        return source
    for text, id, edge, head in deps:
        if int(id) == pos and edge in config.s_dp_list:
            return text
    return text


def get_o_head(deps: List, pos: int, edge, source) -> str:
    text = ''
    for text, id, edge, _ in deps:
        if int(id) == pos and edge in config.o_dp_list:
            return text
    return text


def is_np_head(match, head) -> bool:
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


def get_longest_np(chunks, head: str) -> str:
    longest_np = ''

    for i in range(len(chunks)):
        np = chunks[str(i)]['spanString']
        match = chunks[str(i)]['match']
        match = re.sub(r"\s+", " ", match, flags=re.UNICODE)
        match = match.strip()
        print(head)
        print(np)
        print(match)

        if is_np_head(match, head) and len(np) > len(longest_np):
            longest_np = np

    return longest_np


def extract_spo(deps, chunks, trigger):
    trigger2 = trigger.split(" ")[0]
    p, edge, source = get_trigger(deps, trigger2)
    s_head = get_s_head(deps, p, edge, source)
    o_head = get_o_head(deps, p, edge, source)
    s_np = get_longest_np(chunks, s_head)
    o_np = get_longest_np(chunks, o_head)
    return s_head, s_np, trigger, o_head, o_np
