import os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'credential.json'
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _CREDENTIAL_FILE
google_language_service_client = language.LanguageServiceClient()


def _transform_ner_api_resp(entities, lables=[1, 2, 3]):
    '''
    Transform Google Cloud Natural Language analyze_entities() API response to get_ner output format
    See also get_ner
    @param resp Google Cloud Natrual Language analyze_entities() API response (entities). example 
    @param labels Accepted types, 1 for PERSON, 2 for LOCATION, 3 for ORGANIZATION. see https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity#Type
    '''
    ret = {'person': [], 'location': [], 'organization': []}
    chunk_category_mapping = {1: 'person',
                              2: 'organization',
                              3: 'location'
                              }
    for entity in entities:
        chunk_type = entity.type
        chunk_content = entity.name
        if chunk_type in lables:
            ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


def get_ner(text):
    '''
    Get NER chunks from text
    @return { 'person': [], 'location': [], 'organization': [] }
    '''
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = google_language_service_client.analyze_entities(
        document=document,
        encoding_type='UTF32')

    ner_result = {'person': [], 'location': [], 'organization': []}
    if 'entities' in response:
        ner_result = _transform_ner_api_resp(response.entities)
    return ner_result


if __name__ == '__main__':
    text = 'Tony Bay and John Jones are working at Google in China'
    ner_chunks = get_ner(text)
    print(ner_chunks)
