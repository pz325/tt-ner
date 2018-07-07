import os
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions


_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'credential.json'
)


def _load_credential():
    credential = json.load(open(_CREDENTIAL_FILE))
    return credential


_credential = _load_credential()
_API_VERISON = '2018-03-19'
_natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=_API_VERISON,
    username=_credential['username'],
    password=_credential['password']
)


def _transform_ner_api_resp(entities, lables=['Person', 'Company', 'Location']):
    '''
    Transform IBM Watson Natural Language Understanding /analyze API response to get_ner output format
    See also get_ner
    @param entities IBM Watson Natural Language Understanding /analyze API response (entities). example 
    @param labels Accepted types
    '''
    ret = {'person': [], 'location': [], 'organization': []}
    chunk_category_mapping = {'Person': 'person',
                              'Company': 'organization',
                              'Location': 'location'
                              }
    for entity in entities:
        chunk_type = entity['type']
        chunk_content = entity['text']
        if chunk_type in lables:
            ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


def get_ner(text):
    '''
    Get NER chunks from text
    @return { 'person': [], 'location': [], 'organization': [] }
    '''
    response = _natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions()))

    ner_result = {}
    if 'entities' in response:
        ner_result = _transform_ner_api_resp(response['entities'])
    return ner_result


if __name__ == '__main__':
    text = 'Tony Bay and John Jones are working at Google in China'
    ner_chunks = get_ner(text)
    print(ner_chunks)
