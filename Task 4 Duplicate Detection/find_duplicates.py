#! python3

import sys
import pg8000
from party import Party
from country import Country
from place import Place
from person import Person

def mark_duplicates(elements):
    for i, element in enumerate(elements):
        for j in range(i+1, len(elements)):
            compared_element = elements[j]
            if element.equal(compared_element):
                if element.is_duplicate():
                    # we already have a bucket for those duplicates
                    root_element = element.duplicate_root
                    new_duplicates = [compared_element]
                elif compared_element.is_duplicate():
                    # we have to merge two buckets
                    root_element = compared_element.duplicate_root
                    new_duplicates = [element] + element.duplicates
                else:
                    # open new bucket for duplicates
                    root_element = element
                    new_duplicates = [compared_element]

                for new_duplicate in new_duplicates:
                    if not new_duplicate in root_element.duplicates:
                        root_element.duplicates.append(new_duplicate)
                        new_duplicate.duplicate_root = root_element
            if element.stop_iteration(compared_element):
                break

    return elements

def merge_duplicates(elements):
    for element in elements:
        if len(element.duplicates) > 0:
            merged_element = element
            for duplicate_element in element.duplicates:
                merged_element.merge(duplicate_element)
                merged_element.append_merge_statements(other_party.id)
            yield merged_element

def get_sql_statements(duplicates):
    for duplicate in duplicates:
        yield duplicate.get_update_statement()
        for merge_statement in duplicate.merge_statements:
            yield merge_statement

def main():
    if len(sys.argv) != 5:
        print('Invalid cmd params. Usage: database username password output_file')
        return

    # connect do database
    conn = pg8000.connect(database=sys.argv[1], user=sys.argv[2], password=sys.argv[3])
    cur = conn.cursor()

    # clear output file before the loop below appends to it
    open(sys.argv[4], 'w').close()

    # add new classes that implement Entity's abstract methods
    classes = [Party, Country, Place, Person]
    for cls in classes:
        elements = cls.get_all(cur)
        duplicates = mark_duplicates(elements)
        merged_duplicates = merge_duplicates(elements)
        sql_statements = get_sql_statements(merged_duplicates)

        with open(sys.argv[4], 'a') as f:
            for statement in sql_statements:
                f.write(statement)
                f.write(';\n')

if __name__ == '__main__':
    main()
