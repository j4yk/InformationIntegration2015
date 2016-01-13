from entity import Entity

class Person(Entity):

	primary_key = 'integrated.person.id'
	foreign_references = ['integrated.person_party.person_id']
	# TODO add other references

	def __init__(self, id, first_name, last_name, gender, dbpedia_uri, wikidata_id, birth_year, birth_month, birth_day, birth_name, death_year, death_month, death_day, death_name, occupation):
		super(Person, self).__init__()
		self.id = id
		self.first_name = first_name
		self.last_name = last_name
		self.gender = gender
		self.dbpedia_uri = dbpedia_uri
		self.wikidata_id = wikidata_id
		self.birth_year = birth_year
		self.birth_month = birth_month
		self.birth_day = birth_day
		self.birth_place = birth_name
		self.death_year = death_year
		self.death_month = death_month
		self.death_day = death_day
		self.death_place = death_name
		self.occupation = occupation

	def equal(self, other_person):
		return self.first_name == other_person.first_name

	# values of self are used for the new record
	def merge(self, other_person):
		self.first_name = other_person.first_name + "_new"

	def get_update_statement(self):
		table_name, attribute = self.split_column_name(self.primary_key)
		return 'UPDATE %s SET uri = \'%s\', name = \'%s\' WHERE %s = %i' % (table_name, self.uri, self.name, attribute, self.id)

	@classmethod
	def get_all(self, cursor):
		table_name, attribute = self.split_column_name(self.primary_key)
		cursor.execute("""Select id, first_name, last_name, gender, dbpedia_uri, 
			wikidata_id, birth_year, birth_month, birth_day, birth_name, death_year,
			death_month, death_day, death_name, occupation 
			from (select c.id, c.first_name, c.last_name, c.gender, dbpedia_uri,
			wikidata_id, c.year as birth_year, c.month as birth_month, 
			c.day as birth_day, c.birth_name,   d.year as death_year, 
			d.month as death_month, d.day as death_day, d.name as death_name
			from ( select a.id, a.first_name, a.last_name, a.gender, dbpedia_uri,
			wikidata_id, b.year, b.month, b.day, b.name as birth_name
			from (select * from integrated.person limit 1000) as a 
			left outer join  (  select * from integrated.birth as birth 
			left outer join integrated.place as place on birth.place_id=place.id order By name )
			as b on a.id=b.person_id ) as c left outer join
			(select *  from integrated.death as death left outer join integrated.place 
			on death.place_id = place.id) as d on c.id=d.person_id) as person_birth_death
			left outer join (select person_id, label as occupation from integrated.person_occupation
			left outer join integrated.occupation on occupation_id = id ) o 
			on person_birth_death.id = o.person_id""")
		output = []
		for row in cursor.fetchall():
			output.append(self(*row))
		return output	