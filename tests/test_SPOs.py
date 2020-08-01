from spo.extract import get_fired_trigger, get_trigger_dep, get_s_head, get_o_head, get_longest_np,\
    extract_spo, get_coordinated_nps
from spo.stanzanlp import StanzaNLP
import os

os.environ['CORENLP_HOME'] = './model/stanford-corenlp-4.0.0'


nlp = StanzaNLP()

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


def test_fired_triggers():
    assert 'leads to' == get_fired_trigger(s1)
    assert 'causes' == get_fired_trigger(s2)
    assert 'cause' == get_fired_trigger(s3)
    assert 'inhibit' == get_fired_trigger(s4)
    assert 'cause of' == get_fired_trigger(s5)
    assert None is get_fired_trigger(s6)


def test_s1_trigger():
    deps = nlp.prepare_deps(s1)
    pos, edge, head = get_trigger_dep(deps, 'leads')
    assert 5 == pos
    assert 'root' == edge
    assert 'ROOT' == head


def test_s2_trigger():
    deps = nlp.prepare_deps(s2)
    pos, edge, head = get_trigger_dep(deps, 'causes')
    assert 9 == pos
    assert 'acl:relcl' == edge
    assert 'virus' == head


def test_s1_s_head():
    deps = nlp. prepare_deps(s1)
    assert 'encapsulation' == get_s_head(deps, 5, 'root', 'ROOT')


def test_s1_o_head():
    deps = nlp.prepare_deps(s1)
    assert 'reduction' == get_o_head(deps, 5, 'root', 'ROOT')


def test_s1_chunks():
    chunks = nlp.prepare_chunks(s1)
    assert 'The encapsulation of rifampicin' == chunks[0].spanString


def test_s1_np():
    chunks = nlp.prepare_chunks(s1)
    assert 'The encapsulation of rifampicin' == get_longest_np(chunks, 'encapsulation')
    assert 'a reduction of the Mycobacterium smegmatis inside macrophages' == get_longest_np(chunks, 'reduction')


def test_s1_spo():
    deps = nlp.prepare_deps(s1)
    chunks = nlp.prepare_chunks(s1)
    trigger = 'leads to'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'encapsulation'
    assert s == 'The encapsulation of rifampicin'
    assert p == 'leads to'
    assert o_head == 'reduction'
    assert o == 'a reduction of the Mycobacterium smegmatis inside macrophages'


def test_s2_spo():
    deps = nlp.prepare_deps(s2)
    chunks = nlp.prepare_chunks(s2)
    trigger = 'causes'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'virus'
    assert s == 'the prototype virus'  # TODO
    assert p == 'causes'
    assert o_head == 'gastroenteritis'
    assert o == 'epidemic gastroenteritis'


def test_s3_spo():
    deps = nlp.prepare_deps(s3)
    chunks = nlp.prepare_chunks(s3)
    print(chunks)
    trigger = 'cause'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'exposure'
    assert s == 'the exposure to ambient air pollution'
    assert p == 'cause'
    assert o_head == 'illnesses'
    assert o == 'serious respiratory illnesses'


def test_s4_spo():
    deps = nlp.prepare_deps(s4)
    chunks = nlp.prepare_chunks(s4)
    trigger = 'inhibit'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'ribavirin'
    assert s == 'ribavirin'
    assert p == 'inhibit'
    assert o_head == 'replication'
    assert o == 'SARS coronavirus replication in five different cell types of animal or human origin'


def test_s5_spo():
    deps = nlp.prepare_deps(s5)
    chunks = nlp.prepare_chunks(s5)
    trigger = 'cause of'
    s_head, s, p, o_head, o = extract_spo(deps, chunks, trigger)
    assert s_head == 'infection'
    assert s == 'Chronic hepatitis virus infection'
    assert p == 'cause of'
    assert o_head == 'hepatitis'
    assert o == 'chronic hepatitis, cirrhosis, and hepatocellular carcinoma worldwide'


def test_coordinating_conjunction():
    nps = get_coordinated_nps('chronic hepatitis, cirrhosis, and hepatocellular carcinoma worldwide')
    assert 3 == len(nps)
    assert nps[0] == 'chronic hepatitis'
    assert nps[1] == 'cirrhosis'
    assert nps[2] == 'hepatocellular carcinoma worldwide'


#def test_text():
#    doc = nlp.process(text)
#    assert 5 == len(doc.sentences)


if __name__ == '__main__':
    pass
    # extract_SPOs(text)
