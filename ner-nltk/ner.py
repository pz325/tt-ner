import nltk


def get_ner(text):
    '''
    Get NER chunks from text
    @return { 'person': [], 'location': [], 'organization': [] }
    '''
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    ner_chunks_tree = nltk.ne_chunk(pos_tags)
    return _transform_ner_chunks(ner_chunks_tree)


def _transform_ner_chunks(ner_chunks_tree):
    '''
    Transform NER Chunks to get_ner output format
    See also get_ner
    '''
    ret = {'person': [], 'location': [], 'organization': []}

    chunk_category_mapping = {'PERSON': 'person',
                              'ORGANIZATION': 'organization',
                              'GPE': 'location'
                              }
    for chunk in _traverse_ner_chunks_tree(ner_chunks_tree):
        chunk_type = chunk[0]
        chunk_content = chunk[1]
        ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


def _traverse_ner_chunks_tree(ner_chunks_tree, labels=['PERSON', 'GPE', 'ORGANIZATION']):
    '''
    Traverse NER chunks tree to extract chunks having label in the given labels 
    @return yield list of (LABEL, "chunk content"), e.g. ('PERSON', 'John Jones')
    '''
    try:
        ner_chunks_tree.label()
    except AttributeError:
        pass
    else:
        label = ner_chunks_tree.label()
        if label in labels:
            tokens = [child[0] for child in ner_chunks_tree]
            yield (label, ' '.join(tokens))

        for child in ner_chunks_tree:
            yield from _traverse_ner_chunks_tree(child)


if __name__ == '__main__':
    sentence = 'Mark Blair and John Jones are working at Google in the American.'
    print(get_ner(sentence))
