from spo.data_reader import DataReader
import os

dr = DataReader(os.environ['DATA_DIR'])
it = iter(dr)


def test_num_files():
    pmcid, title, abstract = next(it)
    assert '6954224' == pmcid
    assert 'Enhancing quantum annealing performance by a degenerate two-level system' == title
    assert 'Quantum annealing is an innova' == abstract[:30]

    pmcid, title, abstract = next(it)
    assert '6953918' == pmcid
    assert 'Validity and Reliability of an Instrument for Assessing Self-Care Behaviours ' \
           'in Diabetes Mellitus Type 2 Patients in Binjai City, Indonesia' == title
    assert 'BACKGROUND:Self-care behaviour' == abstract[:30]
