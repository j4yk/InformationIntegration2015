import re

SINGLE_QUOTE = re.compile("'")

def escape(string):
    return SINGLE_QUOTE.subn("''", string)[0]
