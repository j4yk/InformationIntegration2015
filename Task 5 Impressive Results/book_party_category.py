from question import Question
from category import Category

class BookPartyCagetory(Category):
    
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.text_template = 'Welcher Partei gehörte der Autor des Buches "%s" an?'

    def make_question(self):
        self.cursor = self.connection.cursor()
        fact = self.select_tuple_for_question()
        correct_answer = fact[self.PARTY_NAME]
        answers = self.find_more_false_answers_for_question(fact)
        answers.append(correct_answer)
        text = self.text_template % fact[self.BOOK_TITLE]
        self.cursor.close()
        self.cursor = None
        return Question(text, correct_answer, answers)

    def select_tuple_for_question(self):
        self.cursor.execute("""SELECT party.name, book.title, person.first_name || ' ' || person.last_name as name
FROM integrated.person
JOIN integrated.person_party ON person.id = person_party.person_id
JOIN integrated.party ON person_party.party_id = party.id
JOIN integrated.author ON person.id = author.person_id
JOIN integrated.book ON author.person_id = book.author
ORDER BY random() FETCH FIRST 1 ROWS ONLY""")
        return self.cursor.fetchone()

    PARTY_NAME = 0
    BOOK_TITLE = 1
    AUTHOR_NAME = 2

    def find_more_false_answers_for_question(self, fact):
        self.cursor.execute("""SELECT name FROM integrated.party
WHERE name <> %s
ORDER BY random() FETCH FIRST 2 ROWS ONLY""", (fact[self.PARTY_NAME],))
        return [row[0] for row in self.cursor.fetchall()]
