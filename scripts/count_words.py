
import re
import string
import json

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# globals (stopwords) #
stpwrds = set(stopwords.words('english'))
restrictions = json.load(open('qg_restrictions.json', 'r'))
restrictions = restrictions['standard_restrictions']


def count_words(doc_string):
    """

    implements several methods of counting words in a document

    doc_string = document stored as a single string

    """

    tokens = [x.lower() for x in word_tokenize(doc_string.strip())]
    tokens = [x for x in tokens if x not in stpwrds]
    tokens = [x for x in tokens
              if x not in list(string.punctuation)
              and not re.match('\d+\.\d+|\d+|\d+,\d+', x)]
    n_tokens = len(tokens)
    unique_tokens = len(set(tokens))

    ret = {'n_tokens': n_tokens,
           'unique_tokens': unique_tokens}

    total_r = 0
    for x in restrictions:
        ret['n_{0}'.format(x)] = doc_string.count(x)
        total_r += doc_string.count(x)
    ret['total_restrictions'] = total_r

    return ret
