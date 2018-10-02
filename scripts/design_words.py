
# attempt to identify performance VS design standards #

import nltk

from collections import Counter
from nltk.corpus import stopwords


def design_metrics(docs):
    """

    docs = dictionary of parsed document styles produced by
            process_document.process_doc
    tagged_doc = POS-tagged document produced by pos_analysis.tag_document

    takes a POS-tagged document and parses out a number of metrics
    that may or may not identify design-oriented regulations
    """

    # load in design words (aka weights and measures, chemical compounds
    des_wrds = []
    with open("perf_design_words.txt", 'r') as d:
        for l in d:
            des_wrds.append(l.strip())
    des_wrds = [x.lower().strip() for x in des_wrds if x != ""]

    # kill stopwords
    stw = set(stopwords.words('english'))
    des_wrds = [x for x in des_wrds if x not in stw]

    # 1-3 grams in design words list
    dw1 = set([x for x in des_wrds if len(nltk.word_tokenize(x)) == 1])
    dw2 = set([x for x in des_wrds if len(nltk.word_tokenize(x)) == 2])
    dw3 = set([x for x in des_wrds if len(nltk.word_tokenize(x)) == 3])

    # silly count
    sent_tokenized_doc = docs['tokenized_doc']
    tokens = []
    for x in sent_tokenized_doc:
        tokens += x

    maybe_relevant_count = len([x for x in tokens
                                if x in ['standard',
                                         'practice',
                                         'best practice']])

    # single words
    tcount = Counter(tokens)
    dw1_count = [tcount[x] for x in tcount.keys() if x in dw1]

    # bigrams, trigrams
    tbgs = [' '.join(x) for x in nltk.bigrams(tokens)]
    ttgs = [' '.join(x) for x in nltk.trigrams(tokens)]
    tbgs = Counter(tbgs)
    ttgs = Counter(ttgs)
    dw2_count = [tbgs[x] for x in tbgs.keys() if x in dw2]
    dw3_count = [ttgs[x] for x in ttgs.keys() if x in dw3]

    dw_counts = {'design_word_counts': (sum(dw1_count) +
                                        sum(dw2_count) +
                                        sum(dw3_count)),
                 'maybe_relevant_count': maybe_relevant_count,
                 }

    return dw_counts
