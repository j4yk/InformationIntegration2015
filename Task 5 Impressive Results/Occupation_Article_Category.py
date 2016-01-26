#! python3

import sys
import pg8000
from category import Category
from question import Question

class Occupation_Article_Category(Category):
    """Base class for question categories. Inherit from me for a new category"""

    def __init__(self, conn):
        self.question_pattern = """Welchen Beruf hat {}, der auch in einem Artikel 
        mit der Überschrift {} erwähnt wurden?"""
        self.cursor = conn.cursor()

    def make_question(self):
        """Return a new Question to be asked in the Quiz"""
        tuple = self.select_tuple_for_question();
        name = tuple[1] + " " + tuple[2]
        headline = tuple[0]
        occupation = tuple[3]
        answers = [occupation]
        answers.extend(self.find_more_false_answers())
        return Question(self.question_pattern.format(name, headline), occupation, answers)

    def select_tuple_for_question(self):
        self.cursor.execute("""
            select headline, first_name, last_name, label from integrated.person as p
            join integrated.person_article as pa on p.id = pa.person_id
            join integrated.article_header as ah on pa.article_id = ah.id
            join integrated.person_occupation as po on p.id = po.person_id
            join integrated.occupation as o on po.occupation_id = o.id
            order by random() fetch first 1 rows only""")
        return self.cursor.fetchone()

    def find_more_false_answers(self):
        self.cursor.execute("""
            select label from integrated.
            where not (label Like '%,%' or label Like '%-%' or label Like '%.%'
            order by random() fetch first 2 rows only""")

        return self.cursor.fetchall()