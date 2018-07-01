from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import word_tokenize


_tagger = StanfordNERTagger('/Users/Shared/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                            '/Users/Shared/stanford-ner/stanford-ner.jar',
                            encoding='utf-8')


def get_ner(text):
    tokenized = word_tokenize(text)
    ner_chunks = _tagger.tag(tokenized)
    return _transform_ner_chunks(ner_chunks)
    # print(ner_chunks)


def _transform_ner_chunks(ner_chunks, lables=['PERSON', 'LOCATION', 'ORGANIZATION']):
    '''
    Transform NER Chunks to get_ner output format
    See also get_ner
    '''
    ret = {'person': [], 'location': [], 'organization': []}

    chunk_category_mapping = {'PERSON': 'person',
                              'ORGANIZATION': 'organization',
                              'LOCATION': 'location'
                              }
    for chunk in ner_chunks:
        chunk_type = chunk[1]
        chunk_content = chunk[0]
        if chunk_type in lables:
            ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


if __name__ == '__main__':
    sentence = 'Mark Blair and John Jones are working at Google in the America.'
    print(get_ner(sentence))
