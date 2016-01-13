from entity import Entity

class Party(Entity):

    primary_key = 'integrated.party.id'
    foreign_references = ['integrated.person_party.party_id', 'integrated.candidacy.party_id']

    hardcoded_abbreviations = {
        'Cristiani Democratici Uniti': 'CDU (IT)',
        'Christlich Demokratische Union Deutschlands': 'CDU',
        'Christlich-Demokratische Union Deutschlands': 'CDU',
        'Christlich-Soziale Union in Bayern': 'CSU',
        'DIE GRÜNEN': 'B90/DG'
    }

    def __init__(self, id=-1, uri='', name=''):
        super(type(self), self).__init__()
        self.id = id
        self.uri = uri
        self.name = name

    def abbreviation(self):
        if self.name in self.hardcoded_abbreviations.keys():
            return self.hardcoded_abbreviations[self.name]

        output = ""
        for char in self.name:
            if (char != " ") and (not char.islower()):
                output += char
        return output

    def equal(self, other_party):
        if (self.uri is not None) and (other_party.uri is not None):
            return self.uri == other_party.uri
        else:
            return \
                (self.name.lower() == other_party.name.lower()) or \
                ((len(self.abbreviation()) > 2) and (self.abbreviation() == other_party.abbreviation()))

    def merge(self, other_party):
        if other_party.uri != None:
            self.uri = other_party.uri
        if len(other_party.name) > len(self.name):
            self.name = other_party.name

    def get_update_statement(self):
        table_name, attribute = self.split_column_name(self.primary_key)
        return 'UPDATE %s SET uri = \'%s\', name = \'%s\' WHERE %s = %i' % (table_name, self.uri, self.name, attribute, self.id)