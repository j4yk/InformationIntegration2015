from category import Category

class PoliticianWorkCategory(Category):
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'Welches dieser Bücher stammt von %s?'
        self.male_template = 'dem Politiker %s'
        self.female_template = 'der Politikerin %s'

    def answer_in(self, fact):
        return fact[self.WORK_TITLE]

    def format_question(self, fact):
        name = self.make_yellow(fact[self.PERSON_NAME])
        gender = fact[self.PERSON_GENDER]
        if gender == 'f':
            reference = self.female_template % name
        else:
            reference = self.male_template % name
        return self.text_template % (reference)

    def select_tuple_for_question(self):
        self.cursor.execute("""SELECT person.first_name || ' ' || person.last_name AS name, person.gender, work.title AS title
        FROM integrated.person
        JOIN integrated.person_occupation ON person.id = person_occupation.person_id
        JOIN integrated.occupation ON person_occupation.occupation_id = occupation.id
        JOIN (SELECT person_id, name AS title FROM integrated.work
              UNION SELECT book.author AS person_id, title FROM integrated.book) work ON person.id = work.person_id
        WHERE label LIKE '%%Politiker%%' OR label LIKE '%%politiker%%' OR label LIKE '%%Politician%%' OR label LIKE '%%politician%%'
        AND (first_name <> '' or last_name <> '')
ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    PERSON_NAME = 0
    PERSON_GENDER = 1
    WORK_TITLE = 2

    def find_more_false_answers_for_question(self, fact):
        self.cursor.execute("""SELECT title FROM 
(SELECT person_id, name AS title FROM integrated.work
 UNION SELECT author AS person_id, title FROM integrated.book) work
JOIN integrated.person on work.person_id = person.id
WHERE person.first_name || ' ' || person.last_name <> %s
ORDER BY random() FETCH FIRST 2 ROWS ONLY""", (fact[self.PERSON_NAME],))
        return [row[0] for row in self.cursor.fetchall()]
