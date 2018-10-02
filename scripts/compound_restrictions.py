
import re
import json

from nltk.tokenize import word_tokenize

from scripts import untokenize

# globals
restrictions = json.load(open('qg_restrictions.json', 'r'))
restrictions = restrictions['standard_restrictions']


def count_compound_restrictions(tokenized_doc):
    """
    count potential "compound" restrictions #
    general idea: if there's a compound possibility
        (restriction (\d+|[A-Z][a-z]))
    then split off the "header" part (first section)
    and count all the listed paragraph and sub-paragraph tags

    sent_tokenized_doc = a dociment in standard sentence-tokenized form
        i.e. "This is a sentence." should be parsed to
            [['This','is','a','sentence','.'], .... ]

    this can be handled via the process_document function

    """

    docs = tokenized_doc

    # non_cond_len = []
    compounds = {}
    for sent_index in range(0, len(docs)):
        test = untokenize.untokenize(docs[sent_index])
        check1 = re.search('|'.join(['(' + x + ' \([a-z]+\)' + ')'
                                     for x in restrictions]), test)
        check2 = re.search('|'.join(restrictions),
                           re.split('\([^\W\d_]+\)', test)[0])
        if check1 is not None or check2 is not None:
            if check1 is not None:
                test = re.split('|'.join(['(' + x + ' \([a-z]+\)' + ')'
                                          for x in restrictions]), test)
                test = [x for x in test if x is not None]
                test = [' '.join(test[0:2])] + test[2:]
            elif check2 is not None:
                test = [re.split('(\([^\W\d_]+\))', test)[0]] + \
                       [' '.join(re.split('(\([^\W\d_]+\))', test)[1:])]
                test = [x for x in test if x is not None]
                test = [re.sub('(\s)\s+', r'\1', x) for x in test]

            # omit potential conditional compound restrictions
            test2 = re.split('\([^\W\d_]+\)', test[1])
            test2 = [x for x in test2 if len(x) > 10]
            conditionals = [x for x in test2 if re.match(' if|if', x)]
            non_conditionals = [x for x in test2
                                if not re.match(' if|if', x)]

            # count the paragraph/sub-paragraph indicators in the text
            # these should correspond to compound restrictions
            test_count = len([x for x in non_conditionals
                              if len(re.findall('|'.join(restrictions),
                                                x)) == 0])
            test_count2 = len(re.findall('|'.join(restrictions), test[1]))
            added_count = test_count - test_count2
            conditionals_count = len(conditionals)

            # length of compound restriction sets
            if len(non_conditionals) == 0:
                non_cond_len = []
            else:
                non_cond_len = [len(word_tokenize(x))
                                for x in non_conditionals]

            compounds[sent_index] = [test_count, test_count2, added_count,
                                     conditionals_count, non_cond_len]

    compound_groups = len(compounds)
    compound_restrictions = sum([compounds[x][2]
                                 for x in list(compounds.keys())])
    compound_conditionals = sum([compounds[x][3]
                                 for x in list(compounds.keys())])

    ret = {'compound_groups': compound_groups,
           'compound_restrictions': compound_restrictions,
           'compound_conditionals': compound_conditionals}

    return ret
