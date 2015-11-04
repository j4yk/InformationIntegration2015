#! python3

from __future__ import print_function
import sys
import gzip
import psycopg2
# from urllib.request import urlopen
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

def read_items(items, relation):
    conn = psycopg2.connect('dbname=infoint user=infoint password=infoint')
    cursor = conn.cursor()
    counter = 0
    sql = "insert into " + table_name(relation) + " "
    sql_initialized = False
    seq_of_parameters = []
    relations = Relations()
    for item in items:
        item_uri = list(item.keys())[0]
        properties = item[item_uri]
        if not sql_initialized:
            # TODO: change this to reflect the real mapping
            columns = [column_name(relation, prop) for prop in properties.keys() if not is_relational_property(relation, prop)]
            sql += "(uri," \
                + ",".join(prop for prop in columns) \
                + ") values (" \
                + ','.join(['%s'] * (len(columns) + 1)) \
                + ")"
            sql_initialized = True
        parameters = [item_uri]
        seen = set()
        collect_parameters(parameters, item_uri, relations, relation, seen, properties)
        seq_of_parameters.append(parameters)
        counter += 1
        if counter % 100 == 0:
            print(counter, end="\r")
        if counter % 1000 == 1:
            try:
                cursor.executemany(sql, seq_of_parameters)
            except psycopg2.DataError as e:
                import pdb, traceback
                exc_type, value, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)
                sys.exit(1)
            seq_of_parameters[:] = []
        if counter % 5000 == 0:
            conn.commit()
            pass
    cursor.executemany(sql, seq_of_parameters)
    conn.commit()
    relations.insertall(cursor, conn)

def collect_parameters(parameters, item_uri, relations, relation, seen, properties):
    for prop, value in properties.items():
        if value == 'NULL':
            value = None
        if value == '{NULL}': import pdb; pdb.set_trace()
        if is_relational_property(relation, prop):
            relations.add(relation, item_uri, prop, value)
        elif is_array_property(relation, prop):
            parameters.append([value] if type(value) is not list else value)
        else:
            parameters.append(value)

def column_name(relation, property):
    return config[relation, property][COLUMN]

def is_relational_property(relation, property):
    return config[relation, property][TABLE] != "dbpedia_" + relation

def is_array_property(relation, property):
    return config[relation, property][IS_ARRAY]

def table_name(relation):
    return config[relation, "URI"][TABLE]

def name_of_relationship_table(relation, property):
    return config[relation, property][TABLE]

def main():
    import sys, os
    filename = sys.argv[1]
    relation = os.path.basename(filename).replace(".json.gz", "").lower()
    # webstream = urlopen(PERSONS_URL)
    # unzippedstream = gzip.open(webstream)
    load_configuration()
    with open(filename, 'rb') as f:
        unzippedstream = gzip.open(f, 'rt', encoding="utf-8")
        stream = unzippedstream
        read_items(items(stream), relation)

config = {}
TABLE = 0
COLUMN = 1
IS_ARRAY = 2

def load_configuration():
    with open('configuration.txt', 'rt') as f:
        for line in f:
            what, where, is_array = line.split(",")
            is_array = bool(is_array)
            relation, property_uri = what.split(".", 1)
            table, column = where.split(".", 1)
            config[relation, property_uri] = (table, column, is_array)

def items(stream):
    import json
    next(stream)
    for index, line in enumerate(stream):
        json_str = line[:-2]
        if index == 0:
            json_str = json_str[13:]
        yield json.loads(json_str)

if __name__ == '__main__':
    main()
