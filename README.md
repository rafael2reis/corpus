# Quotation Corpus Generator

A tool for processing Bosque and Floresta Corpus.

This project generates a NLP corpus with annotations for Direct and Indirect Quotations for Portuguese. It's based on Bosque and part of Floresta Corpus, both part of [Floresta Sintá(c)tica](http://www.linguateca.pt/floresta/principal.html).

It started as single Python script, but it evolves into an automatic annotator with sofisticated rules. The code need to be refactor in order to future improvements.

## Running

To generate the dataset, on the root folder run:

```
python test_corpus_gen.py
```

The command above generates two files inside the **gen** folder:

* gen/corpus-bosquequotes-train.txt
* gen/corpus-bosquequotes-test.txt

See `corpus_gen.py` for how that is done.

## Rules

The annotation rules are coded in `corpus_annotate.py`. For any changes, like not considering **nosubj**, please modify it.

## Objects

The first step is parsing Bosque and Floresta and create a tree of nodes objects. Each node reflects a node of the *árvores deitadas* format, which is how data in Bosque and Floresta are stored. The script `corpus.py` is responsible for this task.