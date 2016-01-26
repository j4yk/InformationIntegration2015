class Category:
    """Base class for question categories. Inherit from me for a new category"""

    def __init__(self):
        self.question_pattern = '...'

    def make_question(self):
        """Return a new Question to be asked in the Quiz"""
        pass

    def select_tuple_for_question(self):
        pass

    def find_more_false_answers_for_question(self, question):
        # ...
        question.answers.extend(more_answers) # ?
