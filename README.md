# SPO Extractor using Stanza

A dependency parsing-based tool for extracting Subject-Predicate-Object (SPO) triples from biomedical text using Stanford CoreNLP and Stanza.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example Sentences and Universal Dependencies](#example-sentences-and-universal-dependencies)
- [Algorithm](#algorithm)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

## Overview

This tool extracts structured SPO (Subject-Predicate-Object) relationships from natural language sentences, particularly useful for biomedical text mining. It uses dependency parsing patterns and noun phrase chunking to identify semantic relationships between entities.

## Features

- Trigger-based extraction with dependency parsing
- Neural pipeline for accurate dependency analysis
- Support for complex grammatical structures (passive voice, coordinating conjunctions, relative clauses)
- Integration with Stanford CoreNLP's Tregex for chunking
- Stanza's neural models for dependency parsing

## Requirements

- Python 3.x
- Stanford CoreNLP 4.0.0 or later
- Stanza library with English models

## Installation

### 1. Download Stanford CoreNLP

Download and extract the following:
- [Stanford CoreNLP](http://nlp.stanford.edu/software/stanford-corenlp-latest.zip)
- [English models](http://nlp.stanford.edu/software/stanford-corenlp-4.0.0-models-english.jar)

Place the model JAR files in the CoreNLP distribution folder.

### 2. Set Environment Variables

```bash
export CORENLP_HOME=/path/to/stanford-corenlp-full-2020-04-20
export DATA_DIR=/path/to/data/
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Stanza English Model

```bash
python -c 'import stanza; stanza.download("en")'
```

## Usage

### Extract SPO from Input Directory

```bash
PYTHONPATH=. python bin/run_spo.py -i input_directory -o output_file
```

**Parameters:**
- `-i, --input`: Directory containing input text files
- `-o, --output`: Output file for extracted SPO triples

### Test with Example Sentences

```bash
PYTHONPATH=. python tests/test_SPOs.py
```

## Example Sentences and Universal Dependencies

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

### Supported Dependency Patterns

The extractor handles various dependency patterns including:
- **nsubj => VERB => obj**: Basic subject-verb-object
- **nsubj => VERB => obl**: Verb with oblique nominal
- **acl:relcl => VERB => obj**: Relative clauses
- **nsubj:pass => xcomp => VERB => obj**: Passive voice constructions
- **nsubj => NOUN => nmod => conj**: Coordinating conjunctions

## What is Stanza?

Stanza is a Python wrapper that combines Stanford CoreNLP and PyTorch-based NLP models:
- [Tregex](https://nlp.stanford.edu/software/tregex.html) for noun phrase chunking
- Neural pipeline for dependency parsing

## Algorithm

The extraction process follows these steps:

1. **Input Processing**: Accept a sentence and a list of trigger words
2. **Trigger Detection**: Check if any trigger word appears in the sentence
3. **Parsing**: If triggered, run dependency parser and chunker on the sentence
4. **Head Word Identification**: Use dependency relations from the trigger to identify syntactic head words
5. **NP Extraction**: Extract noun phrases by merging dependency relations and chunks based on head words

## Testing

### Run All Tests

```bash
cd /path/to/project-directory
pytest tests/test_SPOs.py
```

### Run Data Reader Tests

```bash
export DATA_DIR="$(pwd)/data/tests"
pytest tests/test_data_reader.py
```

### Test with Example Sentences

```bash
PYTHONPATH=. python tests/test_SPOs.py
```

## Future Enhancements

- **Biomedical NER Integration**: Biomedical Named Entity Recognizers can improve NP chunking and identify semantic roles of noun phrases
- **Entity Type Classification**: Distinguish between different types of biomedical entities (diseases, drugs, proteins, etc.)
- **Relation Classification**: Categorize extracted relationships by type (causation, association, treatment, etc.)
