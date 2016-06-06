"""Analizes NaMo's speeches."""

import logging
import string
from collections import Counter
from pprint import pprint
from string import punctuation as punct

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords
from unidecode import unidecode

from os.path import join as path_join
from src.util import constants as GC

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_hindi_stopwords(filename="stop-words.txt"):
    """Get stopwords in Hindi.

    Args:
    filename - stopwords_set words file

    Returns:
    set of hindi stop words
    """
    stopwords = []
    with open(filename, "r") as stop_words:
        for word in stop_words.readlines():
            stopwords.append(unidecode(word.strip().decode("utf8")))
    return set(stopwords)


def valid_word(word, stop_req=False):
    """Check if word is valid.

    By valid I mean that it's part of a hindi passage and not a stop word

    Args:
    word - token to be checked
    stop_req - if validity is to be checked only for stopwords_set words

    Returns:
    True or False
    """
    if stop_req:
        return word not in stopwords_set
    return len(word.strip()) > 0 and ord(word[0]) > GC.ASCII_LIMIT


def analyze_speeches(filename="1.txt"):
    """Read a speech file.

    Args:
    filename - speech file
    """
    dictionary = corpora.dictionary.Dictionary()
    train_documents = list()
    all_words = list()
    for i in xrange(1, GC.N_SPEECHES):
        filename = path_join(GC.SPEECH_FOLDER, str(i) + ".txt")
        with open(filename, "r") as speech_file:
            speech_words = list()
            for line in speech_file:
                words = line.strip().decode("utf8").split()
                words = [word for word in words if valid_word(word)]
                words = " ".join(map(unidecode, words))
                output = words.translate(string.maketrans("", ""), punct)
                speech_words += [word.lower() for word in output.split()
                                 if valid_word(word, True)]
            all_words += speech_words
            dictionary.add_documents([speech_words])
            train_documents.append(speech_words)
    corpus = [dictionary.doc2bow(text) for text in train_documents]
    lda = LdaModel(corpus=corpus,
                   id2word=dictionary,
                   num_topics=GC.N_TOPICS,
                   passes=10,
                   alpha='auto')

    print '{} topics with corresponding top {} words'.format(GC.N_TOPICS, 10)
    pprint(lda.print_topics())

    word_counter = Counter(all_words)
    print 'Top {} words in {} speeches of NaMo'.format(GC.N_TOP_WORDS,
                                                       GC.N_SPEECHES)
    pprint(word_counter.most_common(GC.N_TOP_WORDS))


if __name__ == "__main__":
    stopwords_set = set(stopwords.words("english"))
    stopwords_file = path_join(GC.MISC_FOLDER, "stop-words.txt")
    stopwords_set = stopwords_set.union(get_hindi_stopwords(stopwords_file))
    analyze_speeches()
