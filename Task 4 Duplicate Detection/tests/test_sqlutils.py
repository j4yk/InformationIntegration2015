from sqlutils import *

def test_escape():
    assert escape("'foo") == "''foo"

def test_to_sql_string():
    assert to_sql_string("fo'o") == "'fo''o'"
    assert to_sql_string(None) == "NULL"
