# SPO extractor

## Example sentences and universal dependencies

![image info](./image/sentence1.png)
* nsubj VERB obl

![image info](./image/sentence2.png)
* _acl:relcl VERB obj

![image info](./image/sentence3.png)
* nsubj VERB obj

![image info](./image/sentence4.png)
* nsubj:pass _xcomp VERB obj

![image info](./image/sentence5.png)
* nsubj NOUN nmod
* NOUN nmod conj

## Usages
* Setting up for
```bash
export CORENLP_HOME=/path/model/
export DATA_DIR=/path/data/
```

* How to install dependencies?
```bash
pip install -r requirements.txt
```

* How to run a test?
```bash
PYTHONPATH=. pytest -p no:warnings tests/test_SPOs.py
PYTHONPATH=. pytest -p no:warnings tests/test_data_reader.py
```

* How to extract SPO?
```bash
PYTHONPATH=. python bin/run_spo.py
```