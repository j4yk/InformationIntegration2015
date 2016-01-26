from category import Category

class CandidacyAlmamaterCagetory(Category):

    POLITICIAN_NAME = 0
    PARLIAMENT_NAME = 1
    UNIVERSITY_NAME = 2
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'An welcher Universität studierte %s, Kandidat bei der Wahl zum Parlament %s?'

    def answer_in(self, fact):
        return fact[self.UNIVERSITY_NAME]

    def format_question(self, fact):
        return self.text_template % (self.make_yellow(fact[self.POLITICIAN_NAME]), self.make_yellow(fact[self.PARLIAMENT_NAME]))

    def select_tuple_for_question(self):
        self.cursor.execute("""
            SELECT (first_name || ' ' || last_name) AS name, parliament.name, university.name FROM
                integrated.person AS p
                JOIN integrated.politician AS pol ON p.id = pol.person_id
                JOIN integrated.candidacy ON p.id = candidacy.candidate
                JOIN integrated.parliament ON candidacy.parliament = parliament.uuid
                JOIN integrated.almamater ON p.id = almamater.person_id
                JOIN integrated.university ON university.uri = almamater.university
            ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    def find_more_false_answers_for_question(self, fact):
        self.cursor.execute("""
            SELECT name FROM integrated.university
            WHERE name <> %s
            ORDER BY random() FETCH FIRST 2 ROWS ONLY""", (fact[self.UNIVERSITY_NAME],))
        return [row[0] for row in self.cursor.fetchall()]
