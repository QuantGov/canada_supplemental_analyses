
import json

from scripts import untokenize
from nltk.tokenize import word_tokenize

# Global Restriction Definition #
restrictions = json.load(open('qg_restrictions.json', 'r'))
restrictions = restrictions['standard_restrictions']


def post_restriction_clause_length(tokenized_doc):
    """

    sent_tokenized_doc = a dociment in standard sentence-tokenized form
        i.e. "This is a sentence." should be parsed to
            [['This','is','a','sentence','.'], .... ]

    this can be handled via the process_document function

    """

    docx = tokenized_doc

    # est length of post-restriction parts of sentences
    post_restr_len = {}
    for x in restrictions:
        post_restr_len[x] = []
    for x in restrictions:
        for k in docx:
            if x in k:
                t = untokenize.untokenize(k)
                try:
                    post_restr = len(word_tokenize(t.split(x)[1]))
                    post_restr_len[x].append(post_restr)
                except IndexError:
                    pass

    return post_restr_len
