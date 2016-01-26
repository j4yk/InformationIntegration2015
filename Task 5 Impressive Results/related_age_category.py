import random
from category import Category

class RelatedAgeCategory(Category):

    RELATIONSHIP_NAME = 0
    OUTLIVE_CHANCE = 1
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'Wie viel Prozent der Leute werden älter als ihr/ihre %s?'

    def answer_in(self, fact):
        return str(fact[self.OUTLIVE_CHANCE])

    def format_question(self, fact):
        return self.text_template % self.make_yellow(fact[self.RELATIONSHIP_NAME])

    def select_tuple_for_question(self):
        self.cursor.execute("""
            SELECT type, 100 - ROUND(100 * SUM(CASE WHEN (d1.year-b1.year) > (d2.year-b2.year) THEN 1 
                ELSE CASE WHEN (d1.year-b1.year) = (d2.year-b2.year) THEN 0.5 ELSE 0 END END) / COUNT(*))
            FROM
                integrated.related_to AS rt
                JOIN integrated.person AS p1 on rt.person1_id = p1.id
                JOIN integrated.person AS p2 on rt.person2_id = p2.id
                JOIN (SELECT * FROM integrated.birth WHERE (year IS NOT NULL)) AS b1 ON p1.id = b1.person_id
                JOIN (SELECT * FROM integrated.birth WHERE (year IS NOT NULL)) AS b2 ON p2.id = b2.person_id
                JOIN (SELECT * FROM integrated.death WHERE (year IS NOT NULL)) AS d1 ON p1.id = d1.person_id
                JOIN (SELECT * FROM integrated.death WHERE (year IS NOT NULL)) AS d2 ON p2.id = d2.person_id
            GROUP BY type
            HAVING COUNT(*) > 20
            ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    def find_more_false_answers_for_question(self, fact):
        result = []
        for _ in range(0, 2):
            number = 0
            while (number == 0) or (number == int(fact[self.OUTLIVE_CHANCE])) or (number in result):
                number = random.randint(30,70)
            result.append(str(number))
        return result
