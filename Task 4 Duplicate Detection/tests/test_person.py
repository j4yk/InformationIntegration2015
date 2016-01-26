#! python3

from person import Person

def test_equal():
	person1 = Person(2015236, "Angela", "Merkel", "f", None, None, None, None, None, None, None, None, None, None, 13790, 1954, 7, 17, None, None, "Hamburg", None, None, None, None, None, "Politikerin", None, None, None, None, None, None, None, None, None)
	person2 = Person(3831874, "Angela", "Merkel", None, None, None, None, None, None, "http://dbpedia.org/resource/Angela_Merkel", None, None, None, None, None, 1954, 7, 17, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1)
	assert person1.equal(person2)

	person1 = Person(1916404, "Adolf", "Hitler", "m", None, None, None, None, None, None, None, None, None, None, 12255, 1889, 4, 20, None, None, "Braunau am Inn", 12006, 1945, 4, 30, "Berlin", "Politiker", None, None, None, None, None, None, None, None, None)
	person2 = Person(3831604, "Adolf", "Hitler", None, None, None, None, None, None, "http://dbpedia.org/resource/Adolf_Hitler", None, None, None, None, None, 1889, 4, 20, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 1)
	assert person1.equal(person2)

def test_had_author_entry():
	person = Person(2156785, "Ben", "Aaronovitc", "m", None, None, None, None, None, None, None, None, None, None, 160572, None, None, None, None, None, "London", None, None, None, None, None, "Schriftsteller", 3020, 3020, 0.0, 0, True, None, None, None, None)
	assert person.had_author_entry == True