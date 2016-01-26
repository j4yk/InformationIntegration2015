class Question:
    """Data object for a question to be asked in the Quiz"""

    def __init__(self, text, correct_answer, answers=None):
        self.text = text
        self.answers = [] if answers is None else answers
        self.correct_answer = correct_answer
