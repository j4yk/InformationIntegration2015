#! python3
import re
from entity import Entity

FIRST_LETTER = re.compile('\\w')

class Place(Entity):
    primary_key = 'integrated.place.id'
    foreign_references = ['integrated.birth.place_id',
            'integrated.death.place_id',
            'integrated.state.capital_id']
    order_clause = 'name'

    def __init__(self, id, name, latitude, longtitude, country_id):
        super().__init__()
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longtitude = longtitude
        self.country_id = country_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        block_ident_match = FIRST_LETTER.search(new_name)
        if block_ident_match:
            self.block_ident = block_ident_match.group().lower()
        else:
            self.block_ident = self._name

    def equal(self, other):
        if self.name == other.name: # TODO: use edit distance carefully?
            sd = self.squared_distance(other)
            if sd is not None and sd > 4:
                return False
            # make sure the countries are deduplicated beforehand!
            if (other.country_id and self.country_id) \
                    != (self.country_id and other.country_id):
                # neither is None and they are different
                return False
            return True
        return False

    def squared_distance(self, other):
        """Returns kind-of distance between two places. This is not geodetically correct."""
        if self.latitude is None or other.latitude is None \
                or self.longtitude is None or other.longtitude is None:
            return None
        return (self.latitude_as_float - other.latitude_as_float)**2 + \
                (self.longtitude_as_float - other.longtitude_as_float)**2

    @property
    def latitude_as_float(self):
        return float(self.latitude.lstrip('NS')) * (-1 if self.latitude[0] == 'S' else 1)

    @property
    def longtitude_as_float(self):
        return float(self.longtitude.lstrip('WE')) * (-1 if self.longtitude[0] == 'W' else 1)

    def merge(self, other):
        if other.name is not None:
            # TODO: check if this is sensible
            self.name = other.name
        if other.latitude is not None:
            self.latitude = other.latitude
        if other.longtitude is not None:
            self.longtitude = other.longtitude
        if other.country_id is not None:
            self.country_id = other.country_id

    def get_update_statement(self):
        table_name, id_attribute = self.split_column_name(self.primary_key)
        return "UPDATE %s SET name = '%s', latitude = '%s', longtitude = '%s', country_id = %s WHERE %s = %i" % (table_name, self.name, self.latitude, self.longtitude, str(self.country_id) if self.country_id is not None else "NULL", self.id)

    def stop_iteration(self, other_place):
        return self.block_ident != other_place.block_ident
        # block ident is set when the name attribute is set
