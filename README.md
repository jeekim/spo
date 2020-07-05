# SPO extractor

## Example sentences and universal dependencies

![image info](./image/sentence1.png)
* The encapsulation of rifampicin leads to a reduction of the Mycobacterium smegmatis inside macrophages.
* nsubj (nominal subject) <= VERB => obl (oblique nominal)

![image info](./image/sentence2.png)
* The Norwalk virus is the prototype virus that causes epidemic gastroenteritis infecting predominantly older children and adults.
* acl:relcl (adjectival clause) => VERB => obj (object)

![image info](./image/sentence3.png)
* It is widely agreed that the exposure to ambient air pollution may cause serious respiratory illnesses and that weather conditions may also contribute to the seriousness.
* nsubj <= VERB => obj

![image info](./image/sentence4.png)
* In this report, ribavirin was shown to inhibit SARS coronavirus replication in five different cell types of animal or human origin at therapeutically achievable concentrations.
* nsubj:pass <= xcomp => VERB => obj

![image info](./image/sentence5.png)
* Chronic hepatitis virus infection is a major cause of chronic hepatitis, cirrhosis, and hepatocellular carcinoma worldwide.
* nsubj <= NOUN => nmod => conj
* coordinating conjunctions

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