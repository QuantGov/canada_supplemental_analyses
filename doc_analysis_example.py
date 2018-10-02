
from scripts import get_document, compound_restrictions, count_words
from scripts import pos_analysis, post_restriction_length
from scripts import process_document, design_words


def main():
    """
    a sample document analysis using the various functions available
    """

    bucket = "quantgov-corpora"
    corpus = "corpus-admincode-canada-consolidated"
    key = "{0}/20180710/clean/C.R.C., c. 1436.txt".format(corpus)

    doc = get_document.get_document(bucket, key)
    docs = process_document.process_doc(doc)

    # compound restriction count
    # i.e. restriction words followed by additional clauses,
    # typically in bullet-point form
    compounds = compound_restrictions.count_compound_restrictions(
            docs['tokenized_doc'])

    # word/token counts
    words = count_words.count_words(docs['clean_text_doc'])

    # part of speech tagger and metrics
    tagged_dcc = pos_analysis.tag_document(docs['sent_tokenized_doc'])
    pos_ratios = pos_analysis.pos_ratios(tagged_dcc)

    # length of clauses following restrictive words
    post_rest = post_restriction_length.post_restriction_clause_length(
            docs['tokenized_doc'])

    # word counts that could indicate design standards
    dwords = design_words.design_metrics(docs)

    print(post_rest)
    print(pos_ratios)
    print(words)
    print(dwords)
    print(compounds)
