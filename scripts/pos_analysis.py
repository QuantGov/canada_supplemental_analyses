
# import boto3
# import json
# import dill as pickle

# from io import BytesIO
from collections import Counter
from nltk import pos_tag

# import POS tagger and associated functions #
# config = json.load(open('config.json', 'r'))
# tagger_locs = config['tagger_locs']


def tag_document(tokenized_doc):
    """
    """

    # killing this for now; load time is annoying for the model
    """
    # get POS tagger from S3 and unpickle for use locally
    pos_model_path = tagger_locs['pos_model_path']
    pos_mdl_support = tagger_locs['pos_mdl_support']
    pos_mdl_support2 = tagger_locs['pos_mdl_support2']

    s3 = boto3.resource('s3')
    with BytesIO() as data:
        s3.Bucket("quantgov-models").download_fileobj(pos_model_path,
                                                      data)
        data.seek(0)  # move back to the beginning after writing
        clf = pickle.load(data)
    with BytesIO() as data:
        s3.Bucket("quantgov-models").download_fileobj(pos_mdl_support,
                                                      data)
        data.seek(0)  # move back to the beginning after writing
        get_cat_word_len = pickle.load(data)
    with BytesIO() as data:
        s3.Bucket("quantgov-models").download_fileobj(pos_mdl_support2,
                                                      data)
        data.seek(0)  # move back to the beginning after writing
        features = pickle.load(data)

    # part of speech analyzer
    tagged_doc = []
    for sentence in sent_tokenized_doc:
        tags = clf.predict([features(sentence, index)
                            for index in range(len(sentence))])
        tagged_doc.append(list(zip(sentence, tags)))
    """

    # NTLK base variant for comparison
    nltk_tags = [pos_tag(x)
                 for x in tokenized_doc]

    return nltk_tags


def pos_ratios(tagged_doc):
    """ """

    # ratio of nouns:verbs
    posd = []
    for x in tagged_doc:
        posd += [k[1] for k in x]
    posd = Counter(posd)
    nvr = ((posd['NN'] + posd['NNS'] + posd['NNP'] + 1) /
           (posd['VB'] + posd['VBD'] + posd['VBG'] + posd['VBN'] +
            posd['VBP'] + posd['VBZ'] + 1))

    ret = {'noun_verb_ratio': nvr,
           'all_counts': posd,
           'n_nouns': (posd['NN'] + posd['NNS'] + posd['NNP']),
           'n_verbs': (posd['VB'] + posd['VBD'] + posd['VBG'] +
                       posd['VBN'] + posd['VBP'] + posd['VBZ']),
           '': ''
           }

    return ret
