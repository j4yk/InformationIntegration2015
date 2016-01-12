#! python3

import sys
import psycopg2
from party import Party
from country import Country
from place import Place

def mark_duplicates(elements):
	for i in range(0, len(elements)):
		for j in range(i+1, len(elements)):
			if elements[i].equal(elements[j]):
				if elements[i].is_duplicate():
					# we already have a bucket for those duplicates
					root_index = elements[i].duplicate_root
					new_indices = [j]
				elif elements[j].is_duplicate():
					# we have to merge two buckets
					root_index = elements[j].duplicate_root
					new_indices = [i] + elements[i].duplicates
				else:
					# open new bucket for duplicates
					root_index = i
					new_indices = [j]

				for new_duplicate in new_indices:
					if not new_duplicate in elements[root_index].duplicates:
						elements[root_index].duplicates.append(new_duplicate)
						elements[new_duplicate].duplicate_root = root_index
            if elements[i].stop_iteration(elements[j]):
                continue

	return elements

def merge_duplicates(elements):
	output = []
	for i in range(0, len(elements)):
		if len(elements[i].duplicates) > 0:
            merged_element = elements[i]
            for j in elements[i].duplicates:
				merged_element.merge(elements[j])
			output.append(merged_element)
	return output

def get_sql_statements(duplicates):
	output = []
	for duplicate in duplicates:
		output = output + [duplicate.get_update_statement()] + duplicate.merge_statements
	return output

def main():
	if len(sys.argv) != 5:
		print('Invalid cmd params. Usage: database username password output_file')
		return

	# connect do database
	conn = psycopg2.connect(database=sys.argv[1], user=sys.argv[2], password=sys.argv[3])
	cur = conn.cursor()

	# clear output file before the loop below appends to it
	open(sys.argv[4], 'w')

	# add new classes that implement Entity's abstract methods
	classes = [Party, Country, Place]
	for cls in classes:
		elements = cls.get_all(cur)
		duplicates = mark_duplicates(elements)
		merged_duplicates = merge_duplicates(elements)
		sql_statements = get_sql_statements(merged_duplicates)
	
		with open(sys.argv[4], 'a') as f:
            f.write(';\n'.join(sql_statements) + ';\n\n')

if __name__ == '__main__':
	main()
