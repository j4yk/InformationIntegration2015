from category import Category

class WorkPartyCagetory(Category):
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'Welcher Partei gehörte der Autor des Werkes %s an?'

    def answer_in(self, fact):
        return fact[self.PARTY_NAME]

    def format_question(self, fact):
        return self.text_template % self.make_yellow(fact[self.WORK_NAME])

    def select_tuple_for_question(self):
        self.cursor.execute("""SELECT party.name, work.name, person.first_name || ' ' || person.last_name as name
FROM integrated.person
JOIN integrated.person_party ON person.id = person_party.person_id
JOIN integrated.party ON person_party.party_id = party.id
JOIN integrated.work ON person.id = work.person_id
ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    PARTY_NAME = 0
    WORK_NAME = 1
    PERSON_NAME = 2

    def find_more_false_answers_for_question(self, fact):
        self.cursor.execute("""SELECT name FROM integrated.party
WHERE name <> %s
ORDER BY random() FETCH FIRST 2 ROWS ONLY""", (fact[self.PARTY_NAME],))
        return [row[0] for row in self.cursor.fetchall()]
