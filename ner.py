import ner_nltk.ner
import ner_nltk.standford_ner
import ner_paralleldots.ner
import ner_google.ner
import ner_ambiverse.ner
import ner_ibm.ner

if __name__ == '__main__':
    sentence = 'Mark Blair and John Jones are working at Google in the American.'
    print(ner_nltk.ner.get_ner(sentence))
    print(ner_nltk.standford_ner.get_ner(sentence))
    print(ner_paralleldots.ner.get_ner(sentence))
    print(ner_google.ner.get_ner(sentence))
    print(ner_ambiverse.ner.get_ner(sentence))
    print(ner_ibm.ner.get_ner(sentence))
