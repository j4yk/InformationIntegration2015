from question import Question
from colorama import Fore, Style

class Category:
    """Base class for question categories. Inherit from me for a new category"""

    def __init__(self):
        self.question_pattern = '...'

    def make_question(self):
        """Return a new Question to be asked in the Quiz"""
        self.cursor = self.connection.cursor()
        try:
            fact = self.select_tuple_for_question()
            correct_answer = self.answer_in(fact)
            answers = self.find_more_false_answers_for_question(fact)
            answers.append(correct_answer)
            text = self.format_question(fact)
            return Question(text, correct_answer, answers)
        finally:
            self.cursor.close()
            self.cursor = None

    def answer_in(self, fact):
        """Return that part of the tuple which is the correct answer"""
        pass

    def select_tuple_for_question(self):
        """Return a tuple which includes the facts from which the question is built"""
        pass

    def find_more_false_answers_for_question(self, fact):
        """Return some fitting candiate answers for the tuple"""
        pass

    def make_yellow(self, text):
        return Style.BRIGHT + Fore.YELLOW + text + Style.RESET_ALL
