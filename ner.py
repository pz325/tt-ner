import os
import hashlib
import diskcache

import ner_nltk.ner
import ner_nltk.standford_ner
import ner_paralleldots.ner
import ner_google.ner
import ner_ambiverse.ner
import ner_ibm.ner


_CACHED_RESULT_PATH = os.path.dirname(os.path.realpath(__file__))


class NER:
    def __init__(self, type):
        self.type = type
        self._cached_results = diskcache.Cache(_CACHED_RESULT_PATH)

    def _get_cache_key(self, text):
        key = '{type}-{text}'.format(type=self.type, text=text)
        key = hashlib.md5(key.encode()).hexdigest()
        return key

    def _get_ner_from_cache(self, text):
        key = self._get_cache_key(text)
        if key in self._cached_results:
            return self._cached_results[key]
        else:
            return None

    def _save_ner_to_cache(self, text, ner_result):
        key = self._get_cache_key(text)
        self._cached_results[key] = ner_result

    def get_ner(self, text):
        pass


class NltkNER(NER):
    def __init__(self):
        NER.__init__(self, 'NltkNER')

    def get_ner(self, text):
        return ner_nltk.ner.get_ner(text)


class StanfordNER(NER):
    def __init__(self):
        NER.__init__(self, 'StanfordNER')

    def get_ner(self, text):
        return ner_nltk.standford_ner.get_ner(text)


class AmbiverseNER(NER):
    def __init__(self):
        NER.__init__(self, 'AmbiverseNER')

    def get_ner(self, text):
        ner_result = self._get_ner_from_cache(text)
        if ner_result:
            print('Get result from local cache')
            return ner_result
        ner_result = ner_ambiverse.ner.get_ner(text)
        self._save_ner_to_cache(text, ner_result)
        return ner_result


class GoogleNER(NER):
    def __init__(self):
        NER.__init__(self, 'GoogleNER')

    def get_ner(self, text):
        ner_result = self._get_ner_from_cache(text)
        if ner_result:
            print('Get result from local cache')
            return ner_result
        ner_result = ner_google.ner.get_ner(text)
        self._save_ner_to_cache(text, ner_result)
        return ner_result


class WatsonNER(NER):
    def __init__(self):
        NER.__init__(self, 'WatsonNER')

    def get_ner(self, text):
        ner_result = self._get_ner_from_cache(text)
        if ner_result:
            print('Get result from local cache')
            return ner_result
        ner_result = ner_ibm.ner.get_ner(text)
        self._save_ner_to_cache(text, ner_result)
        return ner_result


class ParallelDotsNER(NER):
    def __init__(self):
        NER.__init__(self, 'ParallelDotsNER')

    def get_ner(self, text):
        ner_result = self._get_ner_from_cache(text)
        if ner_result:
            print('Get result from local cache')
            return ner_result
        ner_result = ner_paralleldots.ner.get_ner(text)
        self._save_ner_to_cache(text, ner_result)
        return ner_result


if __name__ == '__main__':
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
