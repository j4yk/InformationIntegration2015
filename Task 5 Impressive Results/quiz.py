#! python3

import sys
import pg8000
import colorama
from colorama import Fore, Style
import random

from Occupation_Article_Category import Occupation_Article_Category
from book_party_category import BookPartyCagetory
from work_party_category import WorkPartyCagetory
from candidacy_almamater_category import CandidacyAlmamaterCagetory
from article_party_category import ArticlePartyCategory
from parliament_age_category import ParliamentAgeCategory
from politician_work_category import PoliticianWorkCategory
from related_age_category import RelatedAgeCategory

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else '?' for i in text])

class Quiz:
    """..."""

    right_answers = 0
    wrong_answers = 0
    asked_questions = []

    def __init__(self, categories):
        self.categories = categories

    def ask_questions(self, number):
        """Ask questions until the quiz is over"""
        print("\nWillkommen beim Quiz! Es kommen %s%i%s Fragen." % (Style.BRIGHT + Fore.YELLOW, number, Style.RESET_ALL))
        for question_number in range(1, number+1):
            print("\nFrage %i:" % question_number)
            category = random.choice(self.categories)
            question = category.make_question()
            while question.text in self.asked_questions:
                category = random.choice(self.categories)
                question = category.make_question()
            self.asked_questions.append(question.text)
            self.ask_question(question)

    def ask_question(self, question):
        """Ask a single question"""
        random.shuffle(question.answers)
        print("\n%s\n" % remove_non_ascii(question.text))
        letter = 'A'
        answer_mapping = {}
        for answer in question.answers:
            if answer == question.correct_answer:
                correct_letter = letter
            print("%s%s:%s %s" % (Style.BRIGHT + Fore.YELLOW, letter, Style.RESET_ALL, remove_non_ascii(answer)))
            letter = chr(ord(letter) + 1)

        user_answer = input("\nBitte die Antwort eingeben: ")
        if user_answer == "":
            user_answer = "X"
        elif len(user_answer) > 1:
            user_answer = user_answer[0]
        # if the user enters a char with higher code than any of the answers, we assume it's a lowercase letter and map to the upper case
        if ord(user_answer) >= ord(letter):
            user_answer = chr(ord(user_answer) - 32)

        if user_answer != correct_letter:
            self.wrong_answers += 1
            print("\n%sFalsch.%s Die richtige Antwort ist %s%s%s." 
                % (Style.BRIGHT + Fore.RED, Style.RESET_ALL, Style.BRIGHT + Fore.YELLOW, correct_letter, Style.RESET_ALL))
        else:
            self.right_answers += 1
            print("\n%sRichtig.%s Nicht schlecht!" % (Fore.GREEN, Style.RESET_ALL))
        print("\n" + "-" * 79)

    def show_summary(self):
        """Congratulate or insult the user for his quiz result"""
        print("\nFertig! %s%i%s richtige & %s%i%s falsche Antworten." 
            % (Fore.GREEN, self.right_answers, Style.RESET_ALL, Style.BRIGHT + Fore.RED, self.wrong_answers, Style.RESET_ALL))

def main():
    """Create a quiz and run it"""

    if len(sys.argv) != 5:
        print("Usage: database user password numer_of_questions")
        return

    colorama.init()
    connection = pg8000.connect(database=sys.argv[1], user=sys.argv[2], password=sys.argv[3])
    category_classes = [
            BookPartyCagetory,
            WorkPartyCagetory,
            Occupation_Article_Category,
            CandidacyAlmamaterCagetory,
            ArticlePartyCategory,
            ParliamentAgeCategory,
            PoliticianWorkCategory,
            RelatedAgeCategory,
            ]
    categories = []
    for category_class in category_classes:
        categories.append(category_class(connection))
    
    quiz = Quiz(categories)
    quiz.ask_questions(int(sys.argv[4]))
    quiz.show_summary()
    
    return

if __name__ == '__main__':
    main()
