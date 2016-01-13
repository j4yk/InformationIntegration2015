from entity import Entity
from Levenshtein import distance, jaro_winkler, jaro
from sqlutils import fix_broken_umlauts


class Person(Entity):

    primary_key = 'integrated.person.id'
    foreign_references = [
        'integrated.almamater.person_id',
        'integrated.book.author',
        'integrated.author.person_id',
        'integrated.birth.person_id',
        'integrated.death.person_id',
        'integrated.person_article.person_id',
        'integrated.person_country.person_id',
        'integrated.person_occupation.person_id',
        'integrated.person_party.person_id',
        'integrated.candidacy.candidate',
        'integrated.function.politician',
        'integrated.position.politiican',
        'integrated.politician.person_id',
        'integrated.work.person_id',
        'integrated.related_to.person1_id',
        'integrated.related_to.person2_id',
    ]
    order_clause = 'last_name'

    def __init__(self, id, first_name, last_name, gender, email, url, twitter, degree, education, dbpedia_uri, wikidata_id, 
            nyt_id, articles_count, nyt_def, birth_year, birth_month, birth_day, birth_first_name, birth_last_name, birth_place, 
            death_year, death_month, death_day, death_place, occupation, fans, followers, avg_rating, ratings_count, goodreads_author,
            aw_uuid, aw_username, aw_picture_url):
        self.args = locals()
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
        self.birth_place = fix_broken_umlauts(birth_place)
        self.death_year = death_year
        self.death_month = death_month
        self.death_day = death_day
        self.death_place = fix_broken_umlauts(death_place)
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
              and (self.wikidata_id == other.wikidata_id)
              and (self.dbpedia_uri == other.dbpedia_uri))

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
        assert self.wikidata_id == other.wikidata_id
        assert self.dbpedia_uri == other.dbpedia_uri

        explicit_args = ['id', 'first_name', 'last_name', 'occupation', 'birth_place', 'death_place']
        for arg in self.args:
            if arg in explicit_args:
                continue
            if self.args[arg] is None:
                self.args[arg] = other.args[arg]

        self.first_name = self.longest_string(self.first_name, other.first_name)
        self.last_name = self.longest_string(self.last_name, other.last_name)
        self.occupation = self.longest_string(self.occupation, other.occupation)
        self.birth_place = self.longest_string(self.birth_place, other.birth_place)
        self.death_place = self.longest_string(self.death_place, other.death_place)

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
        cursor.execute("""
            SELECT p.id, p.first_name, p.last_name, p.gender, p.email, p.url, p.twitter, p.degree, p.education,
                p.dbpedia_uri, p.wikidata_id, p.nyt_id, p.associated_articles_count, p.nyt_definition, birth.year, 
                birth.month, birth.day, birth.first_name, birth.last_name, bp.name, death.year, death.month, death.day,
                dp.name, occupation.label, author.fans_count, author.followers_count, author.average_rating,
                author.ratings_count, author.goodreads_author, pol.aw_uuid, pol.aw_username, pol.aw_picture_url
            FROM
                (SELECT * FROM integrated.person FETCH FIRST 10000 ROWS ONLY) AS p
                LEFT OUTER JOIN integrated.birth ON p.id = birth.person_id
                LEFT OUTER JOIN integrated.place AS bp ON birth.place_id = bp.id
                LEFT OUTER JOIN integrated.death ON p.id = death.person_id
                LEFT OUTER JOIN integrated.place AS dp ON death.place_id = dp.id
                LEFT OUTER JOIN integrated.person_occupation AS po ON p.id = po.person_id
                LEFT OUTER JOIN integrated.occupation ON po.occupation_id = occupation.id
                LEFT OUTER JOIN integrated.author ON p.id = author.person_id
                LEFT OUTER JOIN integrated.politician AS pol ON p.id = pol.person_id
            """)
        output = []
        for row in cursor.fetchall():
            output.append(self(*row))
        return output
