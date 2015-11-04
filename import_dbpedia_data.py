#! python3

import sys
import gzip
import ijson
import psycopg2
from urllib.request import urlopen
from collections import defaultdict

PERSONS_URL = "http://web.informatik.uni-mannheim.de/DBpediaAsTables/json/Person.json.gz"

class Relations:
    def __init__(self):
        self.source_relations = set()
        self.instances_by_relation = defaultdict(set)
        self.properties_by_relation = defaultdict(set)
        self.related_values = defaultdict(list)
        self.related_labels = defaultdict(list)

    def add(self, relation, instance_uri, property, related_value):
        self.source_relations.add(relation)
        self.instances_by_relation[relation].add(instance_uri)
        if property.endswith("_label"):
            self.related_labels[relation, instance_uri, trimlabel(property)].append(related_value)
        else:
            self.properties_by_relation[relation].add(property)
            self.related_values[relation, instance_uri, property].append(related_value)

    def insertall(self, cursor, conn):
        for relation in self.source_relations:
            for property in self.properties_by_relation[relation]:
                sql = "insert into " + name_of_relationship_table(relation, property) \
                        + " (source_instance_uri, target_label, target_uri) values (%s, %s, %s)"
                seq_of_parameters = []
                for instance_uri in self.instances_by_relation[relation]:
                    for label, related_uri in zip(
                            self.related_labels[relation, instance_uri, property],
                            self.related_values[relation, instance_uri, property]):
                        seq_of_parameters.append([instance_uri, label, related_uri])
                try:
                    cursor.executemany(sql, seq_of_parameters)
                except:
                    import pdb, traceback
                    type, value, tb = sys.exc_info()
                    traceback.print_exc()
                    pdb.post_mortem(tb)
                conn.commit()
                print("added " + relation + "." + property + " relation tuples")

def trimlabel(property):
    return property[:property.rindex("_label")]

def read_items(items):
    conn = psycopg2.connect('dbname=infoint user=infoint password=infoint')
    cursor = conn.cursor()
    counter = 0
    relation = "foo"
    sql = "insert into " + relation + " "
    sql_initialized = False
    seq_of_parameters = []
    seen_uris = set()
    stop = False
    relations = Relations()
    for item in items:
        item_uri = list(item.keys())[0]
        if item_uri in seen_uris:
            print("WARNING: skipping duplicate instance", item_uri)
            continue
        seen_uris.add(item_uri)
        properties = item[item_uri]
        # TODO: change this to reflect the real mapping
        columns = [column_name(relation, prop) for prop in properties.keys() if not is_relational_property(relation, prop)]
        # 8< remove duplicate column names, should not be needed later
        columns_set = set(columns)
        new_columns = []
        for col in columns:
            if col in columns_set:
                new_columns.append(col)
                columns_set.remove(col)
        columns = new_columns
        # >8
        assert '"relation"' not in columns
        # assert len(column_properties) == len(properties)
        if not sql_initialized:
            sql += "(uri," \
                + ",".join(prop for prop in columns) \
                + ") values (" \
                + ','.join(['%s'] * (len(columns) + 1)) \
                + ")"
            sql_initialized = True
        parameters = [item_uri]
        seen = set()
        for prop, value in properties.items():
            col = column_name(relation, prop)
            # 8< avoid duplicate column names, should not be needed later
            if col in seen:
                continue
            seen.add(col)
            # >8
            if is_relational_property(relation, prop):
                relations.add(relation, item_uri, prop, value)
            elif is_array_property(relation, prop):
                parameters.append([value] if type(value) is not list else value)
            else:
                # 8<
                assert col != '"relation"'
                # >8
                parameters.append(value)
        seq_of_parameters.append(parameters)
        counter += 1
        if counter % 100 == 0:
            print(counter, end="\r")
        if counter % 1000 == 1:
            cursor.executemany(sql, seq_of_parameters)
            seq_of_parameters[:] = []
        if counter % 5000 == 0:
            conn.commit()
        # 8<
        if stop:
            break
        # >8
    cursor.executemany(sql, seq_of_parameters)
    conn.commit()
    relations.insertall(cursor, conn)

def column_name(relation, property):
    s = property[property.rindex('/') + 1:].translate({
        ord('-'): '_',
        ord('#'): '_',
        })
    if not s[0].isalpha():
        s = "_" + s
    return '"' + s + '"'

def is_relational_property(relation, property):
    # TODO: use some real basis for this
    return column_name(relation, property).startswith('"relation')

def is_array_property(relation, property):
    # TODO: use some real basis for this
    return False

def name_of_relationship_table(relation, property):
    return relation + "_" + column_name(relation, property).strip('"')

def main():
    import sys
    webstream = urlopen(PERSONS_URL)
    unzippedstream = gzip.open(webstream)
    items = ijson.items(unzippedstream, 'instances.item')
    read_items(items)
if __name__ == '__main__':
    main()
