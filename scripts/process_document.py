
import re

from nltk.tokenize import sent_tokenize, word_tokenize


def process_doc(doc):
    """
    processing function to clean, parse and tokenize documents
    designed for corpus-canada-consolidated, but should be pretty
    generalizable, aside from a couple of specific reg-ex things

    """

    doc = str(doc)

    # strip weird unicode characters and standardize
    doc2 = doc.encode('ascii', 'ignore')
    doc2 = doc2.decode('unicode_escape').encode('ascii', 'ignore')
    doc2 = doc2.decode('unicode_escape')

    # more cleaning....
    docs = re.sub("b'", "", str(doc2))
    docs = re.sub(u'\x0c', ' ', str(docs))
    docs = re.sub('\\r\\n', ' ', str(docs))
    docs = re.sub('\r', ' ', str(docs))
    docs = re.sub('\n', ' ', str(docs))
    docs = re.sub(r'(\d+)([A-Z]+[a-z]+)',
                  r'\1 \2',
                  docs)

    # replace [Repealed] sections
    # this is only relevant to canada_consolidated, probably
    docs = re.sub('(\[Repealed, .+\])', '', docs)

    # replace brackets I added to segment section headers with punctuation
    # for sentence tokenizer
    docs = docs.replace('[', '. ').replace(']', '. ')

    # similarly, clean up some abbreviations to help sentence tokenizer
    # do it's job better
    docs = re.sub('No\. ', 'No.', docs)
    docs = re.sub(' W\. | w\. ', 'W ', docs)
    docs = re.sub(' S\. | s\. ', 'S ', docs)
    docs = re.sub(' E\. | e\. ', 'E ', docs)
    docs = re.sub(' N\. | n\.', 'N ', docs)

    # and, some general cleaning work
    # docs = re.sub('\n\n(\d+)', '.(1)', docs)
    docs = re.sub('\.\.+', '.', docs)
    docs = re.sub('\s\s+', ' ', docs.strip())
    docs = re.sub('\. \. ', '\. ', docs)
    docs = re.sub('(\d+)([A-Z][a-z])', r'\1 \2', docs)
    docs = re.sub('\\\\', ' ', docs)
    docs = re.sub('(\d+)([^\W\d_]+)', r'\1 \2', docs)
    docs = re.sub('(\([^\W\d_]+\))([^\W\d_]+)', r'\1 \2', docs)
    docs2 = docs
    docs = sent_tokenize(docs, 'english')
    sent_tokenized_doc = docs.copy()
    docs = [word_tokenize(x) for x in docs]
    docs = [x for x in docs if len(x) > 1]

    # last tweaks for pretty sentences, hopefully
    sent_tokenized_doc = [x for x in sent_tokenized_doc
                          if len(x) >= 2]
    sent_tokenized_doc = [re.sub(" \.", "\.", x)
                          for x in sent_tokenized_doc]
    docs2 = re.sub(r"\s/.", r"/.", docs2)
    docs2 = re.sub(r"\s\s+/.", r"/.", docs2)
    docs2 = re.sub(r" [.] ", r"[.] ", docs2)
    docs2 = re.sub(r'\[.\]', r'.', docs2)
    if docs2[0:2] == ". ":
        docs2 = docs2[2:]
    if docs2[-2:] == " '":
        docs2 = docs2[0:-2]

    return {'tokenized_doc': docs,
            'clean_text_doc': docs2,
            'sent_tokenized_doc': sent_tokenized_doc
            }
