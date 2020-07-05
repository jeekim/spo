import unittest
from spo.stanzanlp import StanzaNLP
from spo.utils import get_dependencies, get_fired_trigger, get_trigger_dep, get_s_head, get_o_head, get_longest_np, extract_spo

s1 = 'The encapsulation of rifampicin leads to a reduction of the Mycobacterium smegmatis inside macrophages.'
s2 = 'The Norwalk virus is the prototype virus that causes epidemic gastroenteritis infecting predominantly' \
    ' older children and adults.'
s3 = 'It is widely agreed that the exposure to ambient air pollution may cause serious respiratory illnesses' \
     ' and that weather conditions may also contribute to the seriousness.'
s4 = 'In this report, ribavirin was shown to inhibit SARS coronavirus replication in five different cell types' \
    ' of animal or human origin at therapeutically achievable concentrations.'
s5 = 'Chronic hepatitis virus infection is a major cause of chronic hepatitis, cirrhosis, and hepatocellular' \
    ' carcinoma worldwide.'
s6 = 'This must not be triggered.'
text = s1 + ' ' + s2 + ' ' + s3 + ' ' + s4 + ' ' + s5

# s1_dg = [
#     ('The', '2', 'det'),
#     ('encapsulation', '5', 'nsubj'),
#     ('of', '4', 'case'),
#     ('rifampicin', '2', 'nmod'),
#     ('leads', '0', 'root'),
#     ('to', '8', 'case'),
#     ('a', '8', 'det'),
#     ('reduction', '5', 'obl'),
#     ('of', '12', 'case'),
#     ('the', '12', 'det'),
#     ('Mycobacterium', '12', 'compound'),
#     ('smegmatis', '8', 'nmod'),
#     ('inside', '14', 'case'),
#     ('macrophages', '12', 'nmod'),
#     ('.', '5', 'punct'),
# ]

# s2_dg = [
#     # text, source, edge
#     ('The', '3', 'det'),  # 1
#     ('Norwalk', '3', 'compound'),  # 2
#     ('virus', '7', 'nsubj'),  # 3
#     ('is', '7', 'cop'),  # 4
#     ('the', '7', 'det'),  # 5
#     ('prototype', '7', 'compound'),  # 6
#     ('virus', '0', 'root'),  # 7
#     ('that', '9', 'nsubj'),  # 8
#     ('causes', '7', 'acl:relcl'),  # 9
#     ('epidemic', '11', 'compound'),  # 10
#     ('gastroenteritis', '9', 'obj'),  # 11
#     ('infecting', '9', 'advcl'),  # 12
#     ('predominantly', '14', 'advmod'),  # 13
#     ('older', '15', 'amod'),  # 14
#     ('children', '12', 'obj'),  # 15
#     ('and', '17', 'cc'),  # 16
#     ('adults', '15', 'conj'),  # 17
#     ('.', '7', 'punct'),  # 18
# ]

nlp = StanzaNLP()


def test_triggered():
    assert 'leads to' == get_fired_trigger(s1)
    assert 'causes' == get_fired_trigger(s2)
    assert 'cause' == get_fired_trigger(s3)
    assert 'inhibit' == get_fired_trigger(s4)
    assert 'cause of' == get_fired_trigger(s5)
    assert None is get_fired_trigger(s6)


def test_s1_trigger():
    ann = nlp.process(s1)
    sent = ann.sentences[0]
    deps = get_dependencies(sent)
    pos, edge, head = get_trigger_dep(deps, 'leads')
    assert 5 == pos
    assert 'root' == edge
    assert 'ROOT' == head


def test_s2_trigger():
    ann = nlp.process(s2)
    sent = ann.sentences[0]
    deps = get_dependencies(sent)
    pos, edge, head = get_trigger_dep(deps, 'causes')
    assert 9 == pos
    assert 'acl:relcl' == edge
    assert 'virus' == head


def test_s1_s_head():
    ann = nlp.process(s1)
    sent = ann.sentences[0]
    deps = get_dependencies(sent)
    assert 'encapsulation' == get_s_head(deps, 5, 'root', 'ROOT')


def test_s1_o_head():
    ann = nlp.process(s1)
    sent = ann.sentences[0]
    deps = get_dependencies(sent)
    assert 'reduction' == get_o_head(deps, 5, 'root', 'ROOT')


def test_s1_chunks():
    chunks = nlp.chunk(s1)
    assert 'The encapsulation of rifampicin' == chunks['0']['spanString']


def test_s1_np():
    chunks = nlp.chunk(s1)
    assert 'The encapsulation of rifampicin' == get_longest_np(chunks, 'encapsulation')
    assert 'a reduction of the Mycobacterium smegmatis inside macrophages' == get_longest_np(chunks, 'reduction')


# def test_s1_dg():
#     doc = nlp.process(s1)
#     s = doc.sentences[0]
#     dg = get_dependencies(s)
#     assert s1_dg == dg


def test_s1_spo():
    doc = nlp.process(s1)
    sent = doc.sentences[0]
    deps = get_dependencies(sent)
    chunks = nlp.chunk(s1)
    trigger = 'leads to'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'encapsulation'
    assert s == 'The encapsulation of rifampicin'
    assert p == 'leads to'
    assert o_head == 'reduction'
    assert o == 'a reduction of the Mycobacterium smegmatis inside macrophages'


def test_s2_spo():
    doc = nlp.process(s2)
    sent = doc.sentences[0]
    deps = get_dependencies(sent)
    chunks = nlp.chunk(s2)
    print(chunks)
    trigger = 'causes'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'virus'
    assert s == 'the prototype virus'  # TODO
    assert p == 'causes'
    assert o_head == 'gastroenteritis'
    assert o == 'epidemic gastroenteritis'


def test_s3_spo():
    doc = nlp.process(s3)
    sent = doc.sentences[0]
    deps = get_dependencies(sent)
    chunks = nlp.chunk(s3)
    print(chunks)
    trigger = 'cause'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'exposure'
    assert s == 'the exposure to ambient air pollution'
    assert p == 'cause'
    assert o_head == 'illnesses'
    assert o == 'serious respiratory illnesses'


def test_s4_spo():
    doc = nlp.process(s4)
    sent = doc.sentences[0]
    deps = get_dependencies(sent)
    chunks = nlp.chunk(s4)
    print(chunks)
    trigger = 'inhibit'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    # assert s_head == 'exposure'
    # assert s == 'The encapsulation of rifampicin'
    assert p == 'inhibit'
    assert o_head == 'replication'
    assert o == 'SARS coronavirus replication in five different cell types of animal or human origin'


def test_s5_spo():
    doc = nlp.process(s5)
    sent = doc.sentences[0]
    deps = get_dependencies(sent)
    chunks = nlp.chunk(s5)
    print(chunks)
    trigger = 'cause of'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'infection'
    assert s == 'Chronic hepatitis virus infection'
    assert p == 'cause of'
    assert o_head == 'hepatitis'
    assert o == 'chronic hepatitis, cirrhosis, and hepatocellular carcinoma worldwide'


# @unittest.expectedFailure
def test_text():
    doc = nlp.process(text)
    assert 5 == len(doc.sentences)
