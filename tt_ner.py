import ner
import json
from bs4 import BeautifulSoup

ARTICAL_FILE = 'tt_dev_annotated_articles.json'
NER_RESULT_FILE = 'tt_ner_results.json'
JOB_ERROR_FILE = 'tt_ner_job_errors.json'

ners = [
    ner.NltkNER(),
    # ner.AmbiverseNER(),
    ner.GoogleNER(),
    ner.WatsonNER(),
    ner.ParallelDotsNER()
]


def _strip_html_tag(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def _log_ner_error(e, ner_type, text):
    print('ERROR: {e}'.format(e=e))
    job_error = {
        'ner': ner_type,
        'text': text
    }
    with open(JOB_ERROR_FILE, 'a') as f:
        f.write(json.dumps(job_error))
        f.write('\n')


index = 0
for line in open(ARTICAL_FILE):
    article = json.loads(line)
    title = article['machine_article_title']
    text = article['machine_article_text']
    company_name = article['company_name']

    print('processing: [{index}] - {title}'.format(index=index, title=title))
    ner_result = {}

    for ner_instance in ners:
        print(
            'NER: {type}'.format(type=ner_instance.type))
        ne_in_title = {}
        ne_in_text = {}

        try:
            ne_in_title = ner_instance.get_ner(title)
        except Exception as e:
            _log_ner_error(e, ner_instance.type, title)

        try:
            ne_in_text = ner_instance.get_ner(_strip_html_tag(text))
        except Exception as e:
            _log_ner_error(e, ner_instance.type, text)

        ner_type = ner_instance.type
        ner_result[ner_type] = {
            "ne_in_title": ne_in_title,
            "ne_in_text": ne_in_text
        }

    index += 1
    job_result = {
        "title": title,
        "text": text,
        "compan_name": company_name,
        "ner_result": ner_result
    }

    with open(NER_RESULT_FILE, 'a') as f:
        f.write(json.dumps(job_result))
        f.write('\n')
