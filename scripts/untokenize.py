
import re


def untokenize(words):
    """
    Borrowed from StackOverflow; forget where exactly.
    Idea is quite straight-forward:
    applies a series of rules to reverse NLTK tokenization.
    """

    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"')
    step1 = step1.replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()
