import re

SINGLE_QUOTE = re.compile("'")

def escape(string):
    return SINGLE_QUOTE.subn("''", string)[0]

def to_sql_string(string):
    if string is None:
        return "NULL"
    return "'%s'" % escape(string)
