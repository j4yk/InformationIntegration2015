#! python3

import re
import psycopg2

class Party:

	def __init__(self, id, uri, name):
		self.id = id
		self.uri = uri
		self.name = name.decode('utf-8')
		self.skip = False
		self.duplicates = []

	def abbreviation(self):
		output = ""
		for char in self.name:
			if (char != " ") and (not char.islower()):
				output += char
		return output

# try to execute SQL and swallow exceptions for specified error codes
def executeSQL(cur, sql, ignoreCodes = [], params = () ):
	try:
		cur.execute(sql, params)
	except psycopg2.Error as e:
		if (e.pgcode not in ignoreCodes):
			print("error code: " + e.pgcode)
			raise
	return

def parties_are_equal(party1, party2):
	if (party1.uri is not None) and (party2.uri is not None):
		return party1.uri == party2.uri
	else:
		return \
			(party1.name.lower() == party2.name.lower()) or \
			((len(party1.abbreviation()) > 2) and (party1.abbreviation() == party2.abbreviation()))

def main():
	# connect do database
	conn = psycopg2.connect(database='infoint', user='postgres', password='dbpass')
	cur = conn.cursor()

	executeSQL(cur, "SELECT * FROM integrated.party")
	parties = []
	for row in cur.fetchall():
		party = Party(row[0], row[1], row[2])
		parties.append(party)

	for i in range(0, len(parties)):
		if parties[i].skip:
			continue
		for j in range(i+1, len(parties)):
			if parties[j].skip:
				continue
			if parties_are_equal(parties[i], parties[j]):
				parties[i].duplicates.append(j)
				parties[j].skip = True

	for party in parties:
		if len(party.duplicates) > 0:
			names = [party.name]
			ids = [str(party.id)]
			for dup_id in party.duplicates:
				names.append(parties[dup_id].name)
				ids.append(str(parties[dup_id].id))
			print '\n' + ', '.join(names) + ' [' + ', '.join(ids) + ']'

if __name__ == '__main__':
	main()