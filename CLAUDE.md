# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SPO Extractor is a biomedical text mining tool that extracts Subject-Predicate-Object (SPO) triples from natural language sentences using dependency parsing. It combines Stanford CoreNLP (for noun phrase chunking via Tregex) with Stanza's neural pipeline (for dependency parsing).

## Environment Setup

Before running any code, set required environment variables:

```bash
export CORENLP_HOME=/path/to/stanford-corenlp-full-2020-04-20
export DATA_DIR=/path/to/data/
```

Install dependencies:
```bash
pip install -r requirements.txt
python -c 'import stanza; stanza.download("en")'
```

## Development Commands

### Testing

Run all tests:
```bash
pytest tests/test_SPOs.py
```

Run specific test files:
```bash
export DATA_DIR="$(pwd)/data/tests"
pytest tests/test_data_reader.py
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with nox (automation):
```bash
nox -s tests
```

### Running the Extractor

Extract SPO triples from input directory:
```bash
PYTHONPATH=. python bin/run_spo.py -i input_directory -o output_file
```

Test with example sentences:
```bash
PYTHONPATH=. python tests/test_SPOs.py
```

Note: Always use `PYTHONPATH=.` prefix when running scripts to ensure module imports work correctly.

## Architecture

### Core Components

**spo/extract.py** - SPO extraction logic
- `get_fired_trigger()`: Pattern-matches trigger words in sentences
- `get_trigger_dep()`: Extracts dependency information for triggers
- `get_s_head()` / `get_o_head()`: Identifies subject/object head words using dependency relations
- `get_longest_np()`: Finds longest noun phrase containing a head word
- `extract_spo()`: Main extraction pipeline combining all steps

**spo/stanzanlp.py** - NLP processing wrapper
- `StanzaNLP`: Concrete implementation of NLP interface
- Combines Stanza neural pipeline (dependency parsing) with CoreNLP client (Tregex chunking)
- `process()`: Runs Stanza dependency parser
- `chunk()`: Runs CoreNLP Tregex for NP extraction
- `prepare_deps()` / `prepare_chunks()`: Converts raw annotations to typed data structures

**spo/types.py** - Data structures
- `Edge`: Dependency edge (renamed from `Dep`) - represents a dependency relation
- `Chunk`: Noun phrase chunk with position, span text, and parse tree match
- `Sentence` / `Document`: Higher-level structures (not heavily used)

**spo/config.py** - Configuration
- `triggers`: List of predicate trigger words that fire extraction
- `s_dp_list`: Dependency relations for identifying subjects
- `o_dp_list`: Dependency relations for identifying objects

**spo/data_reader.py** - Input processing
- `DataReader`: Iterator for processing PMC XML files
- Extracts PMCID, title, and abstract from biomedical articles

### Extraction Algorithm

1. **Trigger Detection**: Check if sentence contains trigger word from config
2. **Dependency Parsing**: Run Stanza neural parser on triggered sentence
3. **NP Chunking**: Run CoreNLP Tregex to extract noun phrase chunks
4. **Head Word Identification**: Use dependency relations to find subject/object heads from trigger
5. **NP Expansion**: Match head words to chunks to get full noun phrases
6. **Coordination Handling**: Split coordinated NPs (e.g., "A, B, and C") into separate relations

### Dependency Patterns Handled

The extractor supports multiple grammatical structures:

- **nsubj => VERB => obj**: Basic subject-verb-object (s1)
- **nsubj => VERB => obl**: Verb with oblique nominal (s1)
- **acl:relcl => VERB => obj**: Relative clause constructions (s2)
- **nsubj:pass => xcomp => VERB => obj**: Passive voice with xcomp (s4)
- **nsubj => NOUN => nmod**: Noun-based relations with coordination (s5)

See test_SPOs.py (s1-s5) for concrete examples of each pattern.

## Key Implementation Details

### Edge vs Dep Naming
The data structure was recently renamed from `Dep` to `Edge` to better reflect that it represents a dependency edge in the parse tree.

### NP Head Matching
`is_np_head()` in extract.py:68 uses parse tree patterns to verify a word is the syntactic head of an NP chunk. This handles edge cases like prepositional phrases, conjunctions, and punctuation.

### Recursive Head Finding
`get_s_head()` in extract.py:33 uses recursion for xcomp relations to traverse the dependency tree until finding the actual subject head.

### Stanza Download
Note that `stanza.download('en')` is called at module import time in stanzanlp.py:7, which may cause issues in some environments. This should download models on first run.

### CoreNLP Server
StanzaNLP initializes a CoreNLP server client on port 9001 by default. Ensure CoreNLP server is running or the client will start one automatically (requires CORENLP_HOME to be set).

## Testing Notes

Tests in test_SPOs.py use five example sentences (s1-s5) that demonstrate different grammatical patterns. Each test validates a specific part of the extraction pipeline. The tests assume CORENLP_HOME is set to './model/stanford-corenlp-4.0.0'.
