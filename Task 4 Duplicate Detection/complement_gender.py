#! python3

# psql -c "copy integrated.person to stdout (encoding 'utf-8', delimiter '|', format csv)" > person.csv
# psql -c "copy integrated.person_occupation to stdout (encoding 'utf-8', delimiter '|', format csv)" > person_occupation.csv
# psql -c "copy integrated.occupation to stdout (encoding 'utf-8', delimiter '|', format csv)" > occupation.csv

import re
import csv
from collections import defaultdict

pattern_ends_with_frau = re.compile('[Ff]rau$')

class Data:
    PERSON_ID = 0

    def __init__(self, persons, person_occupations, occupations):
        self.persons_csv = persons
        self.person_occupations_csv = person_occupations
        self.occupations_csv = occupations
        self.read_person_occupations()
        self._occupations = {}

    def read_person_occupations(self):
        self.person_occupations = defaultdict(list)
        for person_occupation in self.person_occupations_csv:
            self.person_occupations[int(person_occupation[0])] \
                    .append(int(person_occupation[1]))

    def id(self, row):
        return int(row[0])

    @property
    def persons(self):
        return self.persons_csv

    def gender(self, person):
        return person[3]

    def set_gender(self, person, new_gender):
        person[3] = new_gender

    def occupations(self, person):
        id = self.id(person)
        return (self.occupation_by_id(occupation_id) \
                for occupation_id in self.person_occupations[id])
    
    def occupation_by_id(self, occupation_id):
        try:
            return self._occupations[occupation_id]
        except KeyError:
            for new_occupation in self.occupations_csv:
                id = self.id(new_occupation)
                self._occupations[id] = new_occupation
                if id == occupation_id:
                    return new_occupation
            raise KeyError("There is no occupation with id %d" % occupation_id)

    def label(self, occupation):
        return occupation[1]

    def add_gender_if_occupation_ends_with_frau(self):
        for person in self.persons:
            try:
                self.id(person)
            except ValueError as e:
                print(e, "skipping this")
                continue
            for occupation in self.occupations(person):
                if pattern_ends_with_frau.search(self.label(occupation)):
                    if self.gender(person) != 'f':
                        self.set_gender(person, 'f')
                        yield person
                    break
            #yield person

psql = 'psql' # dialect name
csv.register_dialect(psql, delimiter='|')

def process_csv_files(person, person_occupation, occupation, output):
    data = Data(persons=csv.reader(person, dialect=psql),
            person_occupations=csv.reader(person_occupation, dialect=psql),
            occupations=csv.reader(occupation, dialect=psql))
    out_csv = csv.writer(output, dialect=psql)
    try:
        for person in data.add_gender_if_occupation_ends_with_frau():
            out_csv.writerow(person)
    except IOError as e:
        import errno
        if e.errno == errno.EPIPE: # pipe has been closed
            return
        raise


if __name__ == '__main__':
    import sys
    import codecs
    try:
        process_csv_files(person=open('person.csv', 'r', encoding='utf-8'),
                person_occupation=open('person_occupation.csv', 'r', encoding='utf-8'),
                occupation=open('occupation.csv', 'r', encoding='utf-8'),
                output=codecs.getwriter('utf-8')(sys.stdout.buffer))
    except Exception as e:
        import pdb
        import traceback
        traceback.print_exc()
        pdb.post_mortem()
