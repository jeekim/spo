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

This tool provides a robust solution for extracting Subject-Predicate-Object (SPO) triples from biomedical text, leveraging the power of dependency parsing to identify and structure complex relationships. By analyzing grammatical dependencies, this extractor identifies the syntactic head of a trigger word and extracts the corresponding noun phrases (NPs) for the subject and object, enabling automated knowledge extraction from unstructured text.

The core of this tool is its ability to process sentences based on a predefined list of trigger words. When a trigger is detected, it initiates a dependency parsing and chunking process using Stanza's neural pipeline and Stanford CoreNLP's Tregex. This allows the system to handle a wide range of grammatical structures, including passive voice, coordinating conjunctions, and relative clauses, making it highly effective for the nuances of biomedical literature.

## Getting Started

This guide will walk you through the essential steps to get the SPO Extractor up and running. For more detailed instructions, please refer to the corresponding sections in this document.

1. **Prerequisites**: Ensure you have Python 3.x, Stanford CoreNLP, and the Stanza library with English models installed.
2. **Environment Setup**: Set the `CORENLP_HOME` and `DATA_DIR` environment variables to point to your CoreNLP installation and data directories.
3. **Run the Extractor**: Use the provided command-line interface to process your input files and generate the extracted SPO triples.

## Features

- **Trigger-Based Extraction**: Initiates the extraction process upon detecting predefined trigger words, ensuring high relevance and precision.
- **Advanced Dependency Parsing**: Utilizes Stanza's neural models for accurate dependency analysis, forming the backbone of the SPO extraction logic.
- **Complex Grammatical Support**: Handles a variety of complex sentence structures, including passive voice, coordinating conjunctions, and relative clauses.
- **Noun Phrase Chunking**: Integrates with Stanford CoreNLP's Tregex to accurately identify and extract noun phrases.
- **Biomedical Focus**: Optimized for biomedical text, making it a valuable tool for researchers and practitioners in the field.

## Requirements

- Python 3.x
- Stanford CoreNLP 4.0.0 or later
- Stanza library with English models

## Installation

To get started with the SPO Extractor, follow these steps:

### Quick Start

For a streamlined setup, you can use the following commands to configure your environment.

```bash
# Set the CORENLP_HOME variable to your Stanford CoreNLP installation
export CORENLP_HOME=/path/to/stanford-corenlp-full-2020-04-20

# Set the DATA_DIR variable to your data directory
export DATA_DIR=/path/to/data/

# Install the required Python packages
pip install -r requirements.txt

# Download the Stanza English model
python -c 'import stanza; stanza.download("en")'
```

### Detailed Steps

1. **Download Stanford CoreNLP**: Download and extract the latest version of [Stanford CoreNLP](http://nlp.stanford.edu/software/stanford-corenlp-latest.zip) and the [English models](http://nlp.stanford.edu/software/stanford-corenlp-4.0.0-models-english.jar).

2. **Configure Environment**: Set the `CORENLP_HOME` environment variable to point to your Stanford CoreNLP installation directory. Additionally, define the `DATA_DIR` variable to specify the location of your input data.

3. **Install Dependencies**: Install the required Python packages using the `requirements.txt` file.

4. **Download Stanza Model**: Download the Stanza English model, which is necessary for the dependency parsing functionality.

## Usage

To extract SPO triples from your text files, run the following command:

```bash
PYTHONPATH=. python bin/run_spo.py --input <input_directory> --output <output_file>
```

### Parameters

- `--input`: Specifies the directory containing the input text files for processing.
- `--output`: Defines the path for the output file where the extracted SPO triples will be saved.

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

## How it Works

The SPO Extractor operates through a series of steps designed to identify and extract structured information from unstructured text.

1. **Input Processing**: The system takes a sentence and a predefined list of trigger words as input.
2. **Trigger Detection**: It scans the sentence to determine if any of the trigger words are present.
3. **Dependency Parsing**: If a trigger is found, the tool initiates a dependency parser and chunker to analyze the grammatical structure of the sentence.
4. **Head Word Identification**: By examining the dependency relations, the extractor identifies the syntactic head of the trigger word.
5. **Noun Phrase Extraction**: Finally, it extracts the relevant noun phrases by merging the dependency relations and chunks corresponding to the subject and object.

## Testing

To ensure the reliability and accuracy of the SPO Extractor, a suite of tests is provided.

### Running All Tests

To execute all tests, navigate to the project directory and run:

```bash
pytest tests/
```

### Running Specific Tests

For more targeted testing, you can run individual test files.

- **SPO Tests**: To test the core SPO extraction functionality, run:
  ```bash
  pytest tests/test_SPOs.py
  ```

- **Data Reader Tests**: To validate the data reading and processing modules, execute:
  ```bash
  export DATA_DIR="$(pwd)/data/tests"
  pytest tests/test_data_reader.py
  ```

## Future Enhancements

To further improve the capabilities of the SPO Extractor, the following enhancements are planned:

- **Biomedical NER Integration**: Incorporating Biomedical Named Entity Recognizers to enhance the accuracy of noun phrase chunking and identify the semantic roles of extracted entities.
- **Entity Type Classification**: Implementing a classification system to distinguish between different types of biomedical entities, such as diseases, drugs, and proteins.
- **Relation Classification**: Developing a model to categorize the extracted relationships into predefined types, including causation, association, and treatment.
