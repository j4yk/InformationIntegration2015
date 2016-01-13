#! python3

from Levenshtein import distance, jaro, median
from entity import Entity
from sqlutils import fix_broken_umlauts

class Occupation(Entity):

    primary_key = 'integrated.occupation.id'
    foreign_references = ['integrated.person_occupation.occupation_id']
    order_clause = 'label'

    female_labels = {}
    female_ids = []

    def __init__(self, id=-1, label=''):
        super(type(self), self).__init__()
        self.id = id
        self.label = fix_broken_umlauts(label)
        self.alt_labels = []

    def is_male_and_female_version(self, str1, str2):
        equal_endings = [ ['e', 'in'], ['er', 'e'], ['', 'in'] ]
        for endings in equal_endings:
            if str1.endswith(endings[0]) and str2.endswith(endings[1]):
                str2 = str2[:-len(endings[1])].replace('ä', 'a') + endings[0]
                break
        else:
            return False
        return str1 == str2

    def gender_equal(self, str1, str2):
        if self.is_male_and_female_version(str1, str2):
            return 2
        elif self.is_male_and_female_version(str2, str1):
            return 1
        else:
            return 0

    def capitalize(self, str):
        return str[0].upper() + str[1:]

    def comparison_label(self):
        return self.label.replace('.', '').replace(' ', '').replace('-', '').replace('?', '').lower()

    def equal(self, other):
        label1 = self.comparison_label()
        label2 = other.comparison_label()

        eq = label1 == label2
        ge = self.gender_equal(label1, label2)
        le = (((len(label1) + len(label2)) / 2.0) / (distance(label1, label2) + 0.0000001)) >= 10
        ja = jaro(label1, label2) > 0.96

        if ge == 1:
            if not self.label in self.female_labels.keys():
                self.female_labels[self.label] = other.label
            self.female_ids.append(self.id)
        elif ge == 2:
            if not other.label in self.female_labels.keys():
                self.female_labels[other.label] = self.label
            self.female_ids.append(other.id)

        return eq or ge or le or ja

    def merge(self, other):
        self.alt_labels.append(self.female_labels.get(other.label, other.label))
        if other.id == self.duplicates[-1].id:
            self.label = median([self.female_labels.get(self.label, self.label)] + self.alt_labels)
            self.label = self.label[0].upper() + self.label[1:]

    def get_update_statement(self):
        table_name, attribute = self.split_column_name(self.primary_key)
        return "UPDATE %s SET label = '%s' WHERE %s = %i" % (table_name, self.label, attribute, self.id)

    def get_class_statements(self):
        output = "UPDATE integrated.person SET gender = 'f' "
        output += "FROM integrated.person_occupation, integrated.occupation "
        output += "WHERE person.id = person_occupation.person_id AND person_occupation.occupation_id = occupation.id "
        output += "AND occupation.id IN (%s)" % str(self.female_ids)[1:-1]
        return [output]

    def stop_iteration(self, other):
        return self.label[0].lower() != other.label[0].lower()
