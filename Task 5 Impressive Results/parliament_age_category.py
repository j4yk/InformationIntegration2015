import random
from category import Category

class ParliamentAgeCategory(Category):

    PARLIAMENT_NAME = 0
    AVERAGE_AGE = 1
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'Was ist das Durchschnittsalter der Abgeordneten im Parlament %s?'

    def answer_in(self, fact):
        return str(fact[self.AVERAGE_AGE])

    def format_question(self, fact):
        return self.text_template % self.make_yellow(fact[self.PARLIAMENT_NAME])

    def select_tuple_for_question(self):
        self.cursor.execute("""
            SELECT parliament.name, ROUND(AVG(2015 - birth.year)) AS avg_age FROM
                integrated.person AS p
                JOIN integrated.birth ON p.id = birth.person_id
                JOIN integrated.candidacy ON p.id = candidacy.candidate
                JOIN integrated.parliament ON candidacy.parliament = parliament.uuid
            GROUP BY parliament.uuid
            HAVING COUNT(*) > 50
            ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    def find_more_false_answers_for_question(self, fact):
        result = []
        for _ in range(0, 2):
            number = 0
            while (number == 0) or (number == int(fact[self.AVERAGE_AGE])) or (number in result):
                number = random.randint(45,58)
            result.append(str(number))
        return result
