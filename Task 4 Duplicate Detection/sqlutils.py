import re

SINGLE_QUOTE = re.compile("'")

def escape(string):
    return SINGLE_QUOTE.subn("''", string)[0]

def to_sql_string(string):
    if string is None:
        return "NULL"
    return "'%s'" % escape(string)

def to_sql_default(value):
	if value is None:
		return "NULL"
	return str(value)

def fix_broken_umlauts(str):
	if str is not None:
		c = u"\u0308"
		return str.replace('a' + c, 'ä').replace('u' + c, 'ü').replace('o' + c, 'ö').replace('A' + c, 'Ä').replace('U' + c, 'U').replace('O' + c, 'o')
	else:
		return None
