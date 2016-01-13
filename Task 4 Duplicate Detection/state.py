#! python3
from entity import Entity
from Levenshtein import distance, jaro_winkler

state_abbrevs = {
    'BW': 'Baden-Württemberg',
    'BY': 'Bayern',
    'BE': 'Berlin',
    'BB': 'Brandenburg',
    'HB': 'Bremen',
    'HH': 'Hamburg',
    "HE": 'Hessen',
    "MV": 'Mecklenburg-Vorpommern',
    'NI': 'Niedersachsen',
    'NW': 'Nordrhein-Westfalen',
    'SN': 'Sachsen',
    "RP": 'Rheinland-Pfalz',
    "SL": 'Saarland',
    "SH": 'Schleswig-Holstein',
    "ST": 'Sachsen-Anhalt',
    "TH": 'Thüringen',
    "Freie Hansestadt Bremen": "Bremen",
    "Freie und Hansestadt Hamburg": "Hamburg",
    "Freistaat Sachsen": "Sachsen",
    "Freistaat Bayern": "Bayern",
    "Freistaat Thüringen": "Thüringen"
}


class State(Entity):
    primary_key = 'integrated.state.id'
    foreign_references = ['integrated.candidacy.state_id']

    def __init__(self, id, name, capital_id, area, population, country_id):
        super().__init__()
        self.id = id
        self.name = name
        self.capital_id = capital_id
        self.area = area
        self.population = population
        self.country_id = country_id

    def equal(self, other):
        if self.name in state_abbrevs:
            return state_abbrevs[self.name] == other.name
        if other.name in state_abbrevs:
            return state_abbrevs[other.name] == self.name
        le = distance(self.name, other.name)
        if len(self.name) > 2 and le < 2:
            return True
        return False

    def merge(self, other):
        if self.name in state_abbrevs:
            self.name = other.name
        if self.capital_id is None:
            self.capital_id = other.capital_id
            self.area = other.area
            self.population = other.population

    def get_update_statement(self):
        print(self.name + " " + str(self.id))
        table_name, id_attribute = self.split_column_name(self.primary_key)
        return "UPDATE %s SET name = '%s', capital_id = '%i', area = '%i', population = '%i', country_id = '%i' WHERE %s = %i" % (table_name, self.name, self.capital_id, self.area, self.population, self.country_id, id_attribute, self.id)
