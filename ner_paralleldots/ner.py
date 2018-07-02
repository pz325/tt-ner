import paralleldots
import os
import json
import hashlib
import diskcache

_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'credential.json'
)


def _load_credential():
    credential = json.load(open(_CREDENTIAL_FILE))
    return credential


# setup paralleldots sdk globally
paralleldots.set_api_key(_load_credential()['api_key'])


def _transform_ner_api_resp(resp, lables=['group', 'name', 'place']):
    '''
    Transform ParallelDots NER API response to get_ner output format
    See also get_ner
    @param resp ParallelDots NER API response in JSON ('entities' field). example 
    [
        {
            'name': 'Google', 
            'confidence_score': 0.970867, 
            'category': 'group'
        }, 
        {
            'name': 'Tony Bay', 
            'confidence_score': 0.830998, 
            'category': 'name'
        }, 
        {
            'name': 'John Jones', 
            'confidence_score': 0.767917, 
            'category': 'name'
        }, 
        {
            'name': 'China', 
            'confidence_score': 0.9739, 
            'category': 'place'
        }
    ]
    '''
    ret = {'person': [], 'location': [], 'organization': []}
    chunk_category_mapping = {'name': 'person',
                              'group': 'organization',
                              'place': 'location'
                              }
    for chunk in resp:
        chunk_type = chunk['category']
        chunk_content = chunk['name']
        if chunk_type in lables:
            ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


def get_ner(text):
    '''
    Get NER chunks from text
    @return { 'person': [], 'location': [], 'organization': [] }
    '''
    ner_api_return = paralleldots.ner(text)
    ner_chunks = _transform_ner_api_resp(ner_api_return['entities'])
    return ner_chunks


if __name__ == '__main__':
    text = 'Tony Bay and John Jones are working at Google in China'
    ner_chunks = get_ner(text)
    print(ner_chunks)
