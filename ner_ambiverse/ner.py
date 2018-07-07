import requests
import json
import os


_auth_token = ''
_CREDENTIAL_FILE = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'credential.json'
)


def _load_credential():
    credential = json.load(open(_CREDENTIAL_FILE))
    return credential


def _auth():
    auth_request_url = 'https://api.ambiverse.com/oauth/token'
    credential = _load_credential()
    auth_request_header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_request_data = [
        ('grant_type', 'client_credentials'),
        ('client_id', credential['client_id']),
        ('client_secret', credential['client_secret'])
    ]

    auth_request = requests.post(
        auth_request_url, data=auth_request_data, headers=auth_request_header)
    auth_token = auth_request.json()['access_token']
    return auth_token


def _transform_ner_api_resp(resp, lables=['PERSON', 'LOCATION', 'ORGANIZATION']):
    '''
    Transform Ambiverse NER API response to get_ner output format
    See also get_ner
    @param resp Ambiverse NER API response in JSON. example 
    [{
        'id': 'http://www.wikidata.org/entity/Q232264', 
        'name': 'San Francisco Bay', 
        'url': 'http://en.wikipedia.org/wiki/San%20Francisco%20Bay', 
        'type': 'LOCATION', 
        'salience': 0.5923567712027171}, 
    {
        'id': 'http://www.wikidata.org/entity/Q314333', 
        'name': 'John Paul Jones', 
        'url': 'http://en.wikipedia.org/wiki/John%20Paul%20Jones', 
        'type': 'PERSON', 
        'salience': 0.44097086336384445}, 
    {
        'id': 'http://www.wikidata.org/entity/Q95', 
        'name': 'Google', 
        'url': 'http://en.wikipedia.org/wiki/Google', 
        'type': 'ORGANIZATION', 
        'salience': 0.22946362923261832}
    ]
    '''
    ret = {'person': [], 'location': [], 'organization': []}
    chunk_category_mapping = {'PERSON': 'person',
                              'ORGANIZATION': 'organization',
                              'LOCATION': 'location'
                              }
    for chunk in resp:
        chunk_type = chunk['type']
        chunk_content = chunk['name']
        if chunk_type in lables:
            ret[chunk_category_mapping[chunk_type]].append(chunk_content)

    return ret


def get_ner(text):
    '''
    Get NER chunks from text
    @return { 'person': [], 'location': [], 'organization': [] }
    '''
    global _auth_token
    if not _auth_token:
        _auth_token = _auth()

    ner_api_url = 'https://api.ambiverse.com/v2/entitylinking/analyze'
    ner_api_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {auth_token}'.format(auth_token=_auth_token)
    }
    ner_data = {
        "confidenceThreshold": "0",
        "docId": "doc1",
        "text": text,
        "language": "en",
        "annotatedMentions": [{"charLength": 3, "charOffset": 5}]
    }
    ner_api_resp = requests.post(
        ner_api_url, headers=ner_api_headers, data=json.dumps(ner_data)).json()

    ner_result = {'person': [], 'location': [], 'organization': []}
    if 'entities' in ner_api_resp:
        ner_result = _transform_ner_api_resp(ner_api_resp.json()['entities'])

    return ner_result


if __name__ == '__main__':
    text = 'Tony Bay and John Jones are working at Google in China'
    ner_chunks = get_ner(text)
    print(ner_chunks)
