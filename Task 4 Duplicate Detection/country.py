#! python3
from entity import Entity

country_abbrevs = {'DE': 'Germany'}
country_translations = {'Deutschland': 'Germany'}

class Country(Entity):
    primary_key = 'integrated.country.id'
    foreign_references = ['integrated.person_country.country_id',
            'integrated.state.country_id',
            'integrated.place.country_id']

    def __init__(self, id, wikidata_id, name):
        super().__init__()
        self.id = id
        self.wikidata_id = wikidata_id
        self.name = name

    def equal(self, other):
        if self.wikidata_id is not None and other.wikidata_id is not None:
            return self.wikidata_id == other.wikidata_id
        if self.name in country_abbrevs:
            return country_abbrevs[self.name] == other.name
        if other.name in country_abbrevs:
            return country_abbrevs[other.name] == self.name
        if self.name in country_translations:
            return country_translations[self.name] == other.name
        if other.name in country_translations:
            return country_translations[other.name] == self.name
        return False

    def merge(self, other):
        if other.wikidata_id is not None:
            self.wikidata_id = other.wikidata_id
        if self.name in country_abbrevs or self.name in country_translations:
            self.name = other.name
        self.append_merge_statements(other.id)

    def get_update_statement(self):
        table_name, id_attribute = self.split_column_name(self.primary_key)
        return "UPDATE %s SET name = '%s', wikidata_id = '%s' WHERE %s = %i" % (table_name, self.name, self.wikidata_id, id_attribute, self.id)
