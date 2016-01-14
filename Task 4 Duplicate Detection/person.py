import string
from entity import Entity
from Levenshtein import distance, jaro_winkler, jaro
from sqlutils import fix_broken_umlauts, to_sql_string, to_sql_default


class Person(Entity):

    primary_key = 'integrated.person.id'
    foreign_references = [
        'integrated.almamater.person_id',
        'integrated.book.author',
        'integrated.person_article.person_id',
        'integrated.person_country.person_id',
        'integrated.person_occupation.person_id',
        'integrated.person_party.person_id',
        'integrated.candidacy.candidate',
        'integrated.function.politician',
        'integrated.position.politician',
        'integrated.work.person_id',
        'integrated.related_to.person1_id',
        'integrated.related_to.person2_id',
    ]
    order_clause = 'last_name'
    partition_index = -1

    def __init__(self, id, first_name, last_name, gender, email, url, twitter, degree, education, dbpedia_uri, wikidata_id, nyt_id, 
            articles_count, nyt_def, birth_place_id, birth_year, birth_month, birth_day, birth_first_name, birth_last_name, birth_place, 
            death_place_id, death_year, death_month, death_day, death_place, occupation, author_fans, author_followers, author_avg_rating, 
            author_ratings_count, author_goodreads_author, politician_aw_uuid, politician_aw_username, politician_aw_picture_url, politician_exists):
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

        self.had_birth_entry = self.needs_entry('birth')
        self.had_death_entry = self.needs_entry('death')
        self.had_author_entry = self.needs_entry('author')
        self.had_politician_entry = self.needs_entry('politician')

    def needs_entry(self, table):
        return any((key.startswith(table + '_') and (self.args[key] is not None)) for key in self.args.keys())

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
              and (self.wikidata_id == None or other.wikidata_id == None or self.wikidata_id == other.wikidata_id)
              and (self.dbpedia_uri == None or other.dbpedia_uri == None or self.dbpedia_uri == other.dbpedia_uri))

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
        explicit_args = ['id', 'first_name', 'last_name', 'occupation', 'birth_place', 'death_place']
        for arg in self.args:
            if arg in explicit_args:
                continue
            if self.args[arg] is None:
                self.args[arg] = other.args[arg]

        self.first_name = self.longest_string(self.first_name, other.first_name)
        self.last_name = self.longest_string(self.last_name, other.last_name)
        self.occupation = self.longest_string(self.occupation, other.occupation)
        if self.longest_string(self.birth_place, other.birth_place) == other.birth_place:
            self.birth_place = other.birth_place
            self.args['birth_place_id'] = other.args['birth_place_id']
        if self.longest_string(self.death_place, other.death_place) == other.death_place:
            self.death_place = other.death_place
            self.args['death_place_id'] = other.args['death_place_id']

        if other.had_birth_entry:
            self.merge_statements.append('DELETE FROM integrated.birth WHERE person_id = %i' % other.id)
        if other.had_death_entry:
            self.merge_statements.append('DELETE FROM integrated.death WHERE person_id = %i' % other.id)
        if other.had_author_entry:
            self.merge_statements.append('DELETE FROM integrated.author WHERE person_id = %i' % other.id)
        if other.had_politician_entry:
            self.merge_statements.append('DELETE FROM integrated.politician WHERE person_id = %i' % other.id)

    def get_update_statements(self):
        table_name, attribute = self.split_column_name(self.primary_key)
        # TODO add birth/death dates and places, occupation to other tables
        yield "UPDATE integrated.person SET (first_name, last_name, gender, email, url, twitter, degree, education, dbpedia_uri, wikidata_id, nyt_id, " \
                + "associated_articles_count, nyt_definition) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE id = %i" \
                % (
                    to_sql_string(self.first_name),
                    to_sql_string(self.last_name),
                    to_sql_string(self.args['gender']),
                    to_sql_string(self.args['email']),
                    to_sql_string(self.args['url']),
                    to_sql_string(self.args['twitter']),
                    to_sql_string(self.args['degree']),
                    to_sql_string(self.args['education']),
                    to_sql_string(self.dbpedia_uri),
                    to_sql_string(self.wikidata_id),
                    to_sql_string(self.args['nyt_id']),
                    to_sql_default(self.args['articles_count']),
                    to_sql_string(self.args['nyt_def']),
                    self.id
                )

        if self.needs_entry('birth'):
            values = (
                to_sql_default(self.args['birth_place_id']),
                to_sql_default(self.args['birth_year']),
                to_sql_default(self.args['birth_month']), 
                to_sql_default(self.args['birth_day']),
                to_sql_string(self.args['birth_first_name']),
                to_sql_string(self.args['birth_last_name']),
                self.id
            )
            if self.had_birth_entry:
                yield "UPDATE integrated.birth SET (place_id, year, month, day, first_name, last_name) = (%s, %s, %s, %s, %s, %s) WHERE person_id = %i" % values
            else:
                yield "INSERT INTO integrated.birth (place_id, year, month, day, first_name, last_name, person_id) VALUES (%s, %s, %s, %s, %s, %s, %i)" % values

        if self.needs_entry('death'):
            values = (
                to_sql_default(self.args['death_place_id']),
                to_sql_default(self.args['death_year']),
                to_sql_default(self.args['death_month']),
                to_sql_default(self.args['death_day']),
                self.id
            )
            if self.had_death_entry:
                yield "UPDATE integrated.death SET (place_id, year, month, day) = (%s, %s, %s, %s) WHERE person_id = %i" % values
            else:
                yield "INSERT INTO integrated.death (place_id, year, month, day, person_id) VALUES (%s, %s, %s, %s, %i)" % values

        if self.needs_entry('author'):
            values = (
                to_sql_default(self.args['author_fans']),
                to_sql_default(self.args['author_followers']), 
                to_sql_default(self.args['author_avg_rating']),
                to_sql_default(self.args['author_ratings_count']),
                to_sql_default(self.args['author_goodreads_author']),
                self.id
            )
            if self.had_author_entry:
                yield "UPDATE integrated.author SET (fans_count, followers_count, average_rating, ratings_count, goodreads_author) = (%s, %s, %s, %s, %s) WHERE person_id = %i" % values
            else:
                yield "INSERT INTO integrated.author (fans_count, followers_count, average_rating, ratings_count, goodreads_author, person_id) VALUES (%s, %s, %s, %s, %s, %i)" % values

        if self.needs_entry('politician'):
            values = (
                to_sql_string(self.args['politician_aw_uuid']),
                to_sql_string(self.args['politician_aw_username']), 
                to_sql_string(self.args['politician_aw_picture_url']),
                self.id
            )
            if self.had_politician_entry:
                yield "UPDATE integrated.politician SET (aw_uuid, aw_username, aw_picture_url) = (%s, %s, %s) WHERE person_id = %i" % values
            else:
                yield "INSERT INTO integrated.politician (aw_uuid, aw_username, aw_picture_url, person_id) = (%s, %s, %s, %i)" % values

    def stop_iteration(self, other):
        # compare only persons with the same starting letter of the lastname
        self_name = self.last_name.lower()
        other_name = other.last_name.lower()
        return len(self_name) == 0 or len(other_name) == 0 or self_name[0] == other_name[0]

    @classmethod
    def get_partition_string(self):
        if self.partition_index < 25:
            self.partition_index += 1
            return "(last_name LIKE '%s') OR (last_name LIKE '%s')" % (string.ascii_lowercase[self.partition_index] + '%%', string.ascii_uppercase[self.partition_index] + '%%'), True
        else:
            return "NOT last_name SIMILAR TO '([A-Z]|[a-z])%%'", False

    @classmethod
    def get_all(self, cursor):
        table_name, attribute = self.split_column_name(self.primary_key)
        partition_string, more_coming = self.get_partition_string()
        print(partition_string)
        cursor.execute("""
            SELECT p.id, p.first_name, p.last_name, p.gender, p.email, p.url, p.twitter, p.degree, p.education,
                p.dbpedia_uri, p.wikidata_id, p.nyt_id, p.associated_articles_count, p.nyt_definition, birth.place_id, birth.year, 
                birth.month, birth.day, birth.first_name, birth.last_name, bp.name, death.place_id, death.year, death.month, death.day,
                dp.name, occupation.label, author.fans_count, author.followers_count, author.average_rating,
                author.ratings_count, author.goodreads_author, pol.aw_uuid, pol.aw_username, pol.aw_picture_url, pol.exists
            FROM
                (SELECT * FROM integrated.person WHERE %s) AS p
                LEFT OUTER JOIN integrated.birth ON p.id = birth.person_id
                LEFT OUTER JOIN integrated.place AS bp ON birth.place_id = bp.id
                LEFT OUTER JOIN integrated.death ON p.id = death.person_id
                LEFT OUTER JOIN integrated.place AS dp ON death.place_id = dp.id
                LEFT OUTER JOIN integrated.person_occupation AS po ON p.id = po.person_id
                LEFT OUTER JOIN integrated.occupation ON po.occupation_id = occupation.id
                LEFT OUTER JOIN integrated.author ON p.id = author.person_id
                LEFT OUTER JOIN (SELECT *, 1 AS exists FROM integrated.politician) AS pol ON p.id = pol.person_id
            ORDER BY p.last_name, p.first_name, occupation.label, p.gender
            """ % partition_string)
        output = []
        for row in cursor.fetchall():
            output.append(self(*row))
        return output, more_coming
