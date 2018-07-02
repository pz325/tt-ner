import paralleldots
import os
import json
import hashlib
import diskcache

_CACHED_RESULT_PATH = os.path.dirname(os.path.realpath(__file__))
_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'credential.json'
)
_cached_results = diskcache.Cache(_CACHED_RESULT_PATH)


def _load_credential():
    credential = json.load(open(_CREDENTIAL_FILE))
    return credential


# setup paralleldots sdk globally
paralleldots.set_api_key(_load_credential()['api_key'])


def _get_ner_from_cache(text):
    global _cached_results
    key = hashlib.md5(text.encode()).hexdigest()
    if key in _cached_results:
        return _cached_results[key]
    else:
        return None


def _save_ner_to_cache(text, ner_result):
    global _cached_results
    key = hashlib.md5(text.encode()).hexdigest()
    _cached_results[key] = ner_result


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
    ret = _get_ner_from_cache(text)
    if ret:
        print('Get resunt from local cache')
        return ret

    ner_api_return = paralleldots.ner(text)
    ner_chunks = _transform_ner_api_resp(ner_api_return['entities'])
    _save_ner_to_cache(text, ner_result)

    return ner_chunks


if __name__ == '__main__':
    text = 'Tony Bay and John Jones are working at Google in China'
    ner_chunks = get_ner(text)
    print(ner_chunks)
