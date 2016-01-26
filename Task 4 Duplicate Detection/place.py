#! python3
import re
from entity import Entity
from sqlutils import escape, to_sql_string, fix_broken_umlauts

FIRST_LETTER = re.compile('\\w')

class Place(Entity):
    primary_key = 'integrated.place.id'
    foreign_references = ['integrated.birth.place_id',
            'integrated.death.place_id',
            'integrated.state.capital_id']
    order_clause = 'name'

    mapping = []
    deleted_ids = []

    def __init__(self, id, name, latitude, longitude, country_id):
        super().__init__()
        self.id = id
        self.name = fix_broken_umlauts(name)
        self.latitude = latitude
        self.longitude = longitude
        self.country_id = country_id

        self.original_values = (self.name, self.latitude, self.longitude, self.country_id)

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
            if sd is not None and sd > 0.1:
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
                or self.longitude is None or other.longitude is None:
            return None
        return (self.latitude_as_float - other.latitude_as_float)**2 + \
                (self.longitude_as_float - other.longitude_as_float)**2

    @property
    def latitude_as_float(self):
        return float(self.latitude.lstrip('NS')) * (-1 if self.latitude[0] == 'S' else 1)

    @property
    def longitude_as_float(self):
        return float(self.longitude.lstrip('WE')) * (-1 if self.longitude[0] == 'W' else 1)

    def merge(self, other):
        if other.name is not None:
            # TODO: check if this is sensible
            self.name = other.name
        if other.latitude is not None:
            self.latitude = other.latitude
        if other.longitude is not None:
            self.longitude = other.longitude
        if other.country_id is not None:
            self.country_id = other.country_id

    def append_merge_statements(self, old_id):
        self.mapping.append((self.id, old_id))
        self.deleted_ids.append(old_id)

    def get_final_class_statements(self):
        for reference in self.foreign_references:
            table_name, attribute = self.split_column_name(reference)
            value_str = str(self.mapping)[1:-1]
            yield "UPDATE %s AS t SET %s = a.new_id FROM (VALUES %s) AS a(new_id, old_id) WHERE %s = a.old_id" % (table_name, attribute, value_str, attribute)
        yield "DELETE FROM integrated.place WHERE id IN (%s)" % str(self.deleted_ids)[1:-1]

    def get_update_statements(self):
        if (self.name, self.latitude, self.longitude, self.country_id) != self.original_values:
            table_name, id_attribute = self.split_column_name(self.primary_key)
            yield "UPDATE %s SET name = '%s', latitude = %s, longitude = %s, country_id = %s WHERE %s = %i" \
                    % (table_name,
                            escape(self.name),
                            to_sql_string(self.latitude),
                            to_sql_string(self.longitude),
                            str(self.country_id) if self.country_id is not None else "NULL",
                            id_attribute,
                            self.id)

    def stop_iteration(self, other_place):
        #b = self.name[0].lower() != other_place.name[0].lower()
        b = self.block_ident != other_place.block_ident
        if b:
            try:
                print(self.name)
                #print(self.block_ident + '   ' + other_place.block_ident)
            except:
                pass
        return b
        # block ident is set when the name attribute is set
