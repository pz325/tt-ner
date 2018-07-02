# Named Entity Recognition (NER) survey for TT

## Include

- NLTK NER (`nltk/ner.py`)
- Stanford NER (`nltk/stanford_ner.py`)
- Ambiverse Entity Linking Service API (`ambiverse/ner.py`)
- Google Cloud Natural Language API (`google/ner.py`)
- ParallelDots API (`paralleldots/ner.py`)
- IBM Watson Natural Language Understanding API (`ibm/ner.py`)

## Prepare

```
pip install -r requirements.txt
```

- [Ambiverse API](ner_ambiverse/README.md)
- [Google Cloud Natural Language API](ner_google/README.md)
- [ParallelDots API](ner_paralleldots/README.md)
- [IBM Watson Natural Language Understanding API](ner_ibm/README.md)

## Usage

Refer to `ner.py`

```
sentence = 'Mark Blair and John Jones are working at Google in the American.'
nltkNER = NltkNER()
print(nltkNER.type)
print(nltkNER.get_ner(sentence))

stanfordNER = StanfordNER()
print(stanfordNER.type)
print(stanfordNER.get_ner(sentence))

ambiverseNER = AmbiverseNER()
print(ambiverseNER.type)
print(ambiverseNER.get_ner(sentence))

googleNER = GoogleNER()
print(googleNER.type)
print(googleNER.get_ner(sentence))

watsonNER = WatsonNER()
print(watsonNER.type)
print(watsonNER.get_ner(sentence))

parallelDotsNER = ParallelDotsNER()
print(parallelDotsNER.type)
print(parallelDotsNER.get_ner(sentence))
```
