from sqlutils import *

def test_escape():
    assert escape("'foo") == "''foo"
