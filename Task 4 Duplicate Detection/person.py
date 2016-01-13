from entity import Entity
from Levenshtein import distance, jaro_winkler, jaro
from sqlutils import fix_broken_umlauts


class Person(Entity):

    primary_key = 'integrated.person.id'
    foreign_references = [
        'integrated.almamater.person_id',
        'integrated.author.person_id',
        'integrated.birth.person_id',
        'integrated.death.person_id',
        'integrated.person_article.person_id',
        'integrated.person_country.person_id',
        'integrated.person_occupation.person_id',
        'integrated.person_party.person_id',
        'integrated.politician.person_id',
        'integrated.work.person_id',
        'integrated.related_to.person1_id',
        'integrated.related_to.person2_id',
    ]
    order_clause = 'last_name'

    def __init__(self, id, first_name, last_name, gender, dbpedia_uri, wikidata_id, birth_year, birth_month, birth_day, birth_name, death_year, death_month, death_day, death_name, occupation):
        super(Person, self).__init__()
        self.id = id
        self.first_name = fix_broken_umlauts(first_name)
        self.last_name = fix_broken_umlauts(last_name)
        self.gender = gender
        self.dbpedia_uri = dbpedia_uri
        self.wikidata_id = wikidata_id
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.birth_place = fix_broken_umlauts(birth_name)
        self.death_year = death_year
        self.death_month = death_month
        self.death_day = death_day
        self.death_place = fix_broken_umlauts(death_name)
        self.occupation = fix_broken_umlauts(occupation)

    def equal(self, other):
        # exclude identical tuples
        if (self.id == other.id):
            return False

        # exclude empty names
        if (len(self.first_name) < 1 or len(other.first_name) < 1 or len(self.last_name) < 1 or len(other.last_name) < 1):
            return False
        self_name = self.first_name + " " + self.last_name
        other_name = other.first_name + " " + other.last_name
        le_first = distance(self.first_name, other.first_name) / ((len(self.first_name)+len(other.first_name))/20)
        le_last = distance(self.last_name, other.last_name) / ((len(self.last_name)+len(other.last_name))/20)
        jw_first = jaro(self.first_name, other.first_name)
        jw_last = jaro_winkler(self.last_name, other.last_name)
        if (self.occupation == None):
            self.occupation = ""
        if (other.occupation == None):
            other.occupation = ""
        jw_occupation = jaro_winkler(self.occupation, other.occupation)
        result = ((le_first <= 1.18 and le_last <= 1.18)
              and (jw_last >= 0.95 and jw_first >= 0.95)
              and (self.birth_year == None or other.birth_year == None or abs(int(self.birth_year) - int(other.birth_year)) < 5)
              and (self.death_year == None or other.death_year == None or abs(int(self.death_year) - int(other.death_year)) < 5)
              and (self.gender == other.gender or self.gender is None or other.gender is None)
              and (jw_occupation >= 0.9 or self.occupation == "" or other.occupation == "")
              and (self.birth_place == None or other.birth_place == None or jaro_winkler(self.birth_place, other.birth_place) >= 0.7)
              and (self.death_place == None or other.death_place == None or jaro_winkler(self.death_place, other.death_place) >= 0.7)
              and (self.wikidata_id == other.wikidata_id or (self.wikidata_id == None and other.wikidata_id == None))
              and (self.dbpedia_uri == other.dbpedia_uri or (self.dbpedia_uri == None and other.dbpedia_uri == None)))

        if result == True:
            string = str(self.id) + "|" + self_name + "|" + other_name + "|" + str(other.id) + "|" + str(le_first) + "|" + str(jw_first) + "|" + str(le_last) + "|" + str(jw_last)
            print(string.encode('utf-8'))
        return result

    def longest_string(self, s1, s2):
        if s1 == None or (s2 != None and len(s1) < len(s2)):
            return s2
        return s1

    # values of self are used for the new record
    def merge(self, other):
        # TODO dates
        self.first_name = self.longest_string(self.first_name, other.first_name)
        self.last_name = self.longest_string(self.last_name, other.last_name)
        self.occupation = self.longest_string(self.occupation, other.occupation)
        self.birth_place = self.longest_string(self.birth_place, other.birth_place)
        self.death_place = self.longest_string(self.death_place, other.death_place)
        self.wikidata_id = self.longest_string(self.wikidata_id, other.wikidata_id)
        self.dbpedia_uri = self.longest_string(self.dbpedia_uri, other.dbpedia_uri)
        if self.gender is None:
            self.gender = other.gender

    def get_update_statements(self):
        table_name, attribute = self.split_column_name(self.primary_key)
        # TODO add birth/death dates and places, occupation to other tables
        return ["UPDATE %s SET first_name = '%s', last_name = '%s', gender = '%s', wikidata_id = '%s', dbpedia_uri = '%s' WHERE %s = %i" % (table_name, self.first_name, self.last_name, self.gender, self.wikidata_id, self.dbpedia_uri, attribute, self.id)]

    def stop_iteration(self, other):
        # compare only persons with the same starting letter of the lastname
        self_name = self.last_name.lower()
        other_name = other.last_name.lower()
        return len(self_name) == 0 or len(other_name) == 0 or self_name[0] == other_name[0]

    @classmethod
    def get_all(self, cursor):
        table_name, attribute = self.split_column_name(self.primary_key)
        # TODO remove limit from integrated.person
        cursor.execute("""Select id, first_name, last_name, gender, dbpedia_uri, 
            wikidata_id, birth_year, birth_month, birth_day, birth_name, death_year,
            death_month, death_day, death_name, occupation 
            from (select c.id, c.first_name, c.last_name, c.gender, dbpedia_uri,
            wikidata_id, c.year as birth_year, c.month as birth_month, 
            c.day as birth_day, c.birth_name,   d.year as death_year, 
            d.month as death_month, d.day as death_day, d.name as death_name
            from ( select a.id, a.first_name, a.last_name, a.gender, dbpedia_uri,
            wikidata_id, b.year, b.month, b.day, b.name as birth_name
            from (select * from integrated.person limit 1000000) as a 
            left outer join  (  select * from integrated.birth as birth 
            left outer join integrated.place as place on birth.place_id=place.id order By name )
            as b on a.id=b.person_id ) as c left outer join
            (select *  from integrated.death as death left outer join integrated.place 
            on death.place_id = place.id) as d on c.id=d.person_id) as person_birth_death
            left outer join (select person_id, label as occupation from integrated.person_occupation
            left outer join integrated.occupation on occupation_id = id ) o 
            on person_birth_death.id = o.person_id
            order by last_name, first_name, occupation, gender""")
        output = []
        for row in cursor.fetchall():
            output.append(self(*row))
        return output
