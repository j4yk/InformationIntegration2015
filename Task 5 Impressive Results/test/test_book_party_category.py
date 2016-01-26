import pytest
from book_party_category import BookPartyCagetory
import pg8000

@pytest.fixture(scope='module')
def conn():
    import os
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'test-database.ini'))
    try:
        return pg8000.connect(**config['integrated-database'])
    except KeyError:
        raise Exception("You must supply database credentials in test/test-database.ini")

def test_make_question(conn):
    cat = BookPartyCagetory(conn)
    question = cat.make_question()
    assert str(question.text) == question.text, "answer should be str"
    assert str(question.correct_answer) == question.correct_answer, "answer should be str"
    assert len(question.answers) == 3, "want exactly three answers"
    for i, answer in enumerate(question.answers):
        for j, other_answer in enumerate(question.answers):
            assert i == j or answer != other_answer, "duplicate answer"
