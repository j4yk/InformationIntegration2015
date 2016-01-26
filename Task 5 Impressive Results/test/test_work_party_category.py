from work_party_category import WorkPartyCagetory
from test.connection import conn

def test_make_question(conn):
    cat = WorkPartyCagetory(conn)
    question = cat.make_question()
    assert str(question.text) == question.text, "answer should be str"
    assert str(question.correct_answer) == question.correct_answer, "answer should be str"
    assert len(question.answers) == 3, "want exactly three answers"
    for i, answer in enumerate(question.answers):
        for j, other_answer in enumerate(question.answers):
            assert i == j or answer != other_answer, "duplicate answer"
