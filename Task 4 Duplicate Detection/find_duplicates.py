#! python3

import sys
import pg8000
from party import Party
from country import Country
from place import Place
from person import Person
from state import State
from occupation import Occupation

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
                    element.duplicates = []
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
                merged_element.append_merge_statements(duplicate_element.id)
            yield merged_element

def get_sql_statements(duplicates):
    append_class_statements = True
    for duplicate in duplicates:
        if append_class_statements:
            for class_statement in duplicate.get_class_statements():
                yield class_statement
            append_class_statements = False
        yield duplicate.get_update_statement()
        for merge_statement in duplicate.merge_statements:
            yield merge_statement

def main():
    if len(sys.argv) != 4:
        print('Invalid cmd params. Usage: database username password')
        return

    # connect do database
    conn = pg8000.connect(database=sys.argv[1], user=sys.argv[2], password=sys.argv[3])
    cur = conn.cursor()

    # add new classes that implement Entity's abstract methods
    classes = [Party, Country, Place, Person, State, Occupation]
    for cls in classes:
        elements = cls.get_all(cur)
        duplicates = mark_duplicates(elements)
        merged_duplicates = merge_duplicates(elements)
        sql_statements = get_sql_statements(merged_duplicates)

        with open('output_' + cls.__name__.lower() + '.txt', 'w', encoding='utf-8') as f:
            for statement in sql_statements:
                f.write(statement)
                f.write(';\n')

if __name__ == '__main__':
    main()
