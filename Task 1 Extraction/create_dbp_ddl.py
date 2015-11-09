#! python3

import sys
import json
import os
import gzip

datatype_map = {
    'http://dbpedia.org/datatype/squareMetre': 'REAL',
    'http://dbpedia.org/datatype/squareKilometre': 'REAL',
    'http://dbpedia.org/datatype/inhabitantsPerSquareKilometre': 'REAL',
    'http://www.w3.org/2000/01/rdf-schema#Literal': 'TEXT',
    'http://www.w3.org/2001/XMLSchema#string': 'TEXT',
    'http://www.w3.org/2001/XMLSchema#nonNegativeInteger': 'INT',
    'http://www.w3.org/2001/XMLSchema#double': 'REAL',
    'http://www.w3.org/2001/XMLSchema#date': 'DATE',
    'http://www.w3.org/2001/XMLSchema#boolean': 'BOOLEAN',
    'http://www.w3.org/2001/XMLSchema#float': 'REAL',
    'http://www.w3.org/2001/XMLSchema#integer': 'BIGINT',
    'http://www.w3.org/2002/07/owl#Thing': 'TEXT',
    'http://dbpedia.org/datatype/minute': 'INT',
    'http://www.w3.org/2001/XMLSchema#gYear': 'INT',
    'http://dbpedia.org/datatype/cubicMetrePerSecond': 'REAL',
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString': 'TEXT',
    'http://www.w3.org/2001/XMLSchema#positiveInteger': 'INT',
    'http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing': 'TEXT',
    'http://www.w3.org/2001/XMLSchema#gYearMonth': 'DATE',
    'http://www.openlinksw.com/schemas/virtrdf#Geometry': 'TEXT',
    'http://www.w3.org/2000/01/rdf-schema#Class': 'TEXT',
    'http://dbpedia.org/datatype/millimetre': 'REAL',
    'http://dbpedia.org/datatype/centimetre': 'REAL',
    'http://dbpedia.org/datatype/kilogram': 'REAL',
    'http://dbpedia.org/datatype/engineConfiguration': 'TEXT',
}

# find all .json.gz files
def process_dir(name):
    create_statements = []
    alter_statements = []
    drop_statements = []
    clear_configuration_file()
    if os.path.isdir(name):
        for file_name in sorted(os.listdir(name)):
            if (file_name.endswith(".json.gz")):
                full_file_name = os.path.join(name, file_name)
                create_statements, alter_statements, drop_statements = process_file(full_file_name, create_statements, alter_statements, drop_statements)
        write_statements_to_file(create_statements, alter_statements, drop_statements)
    return

def process_file(name, create_statements, alter_statements, drop_statements):
    print("Processing '" + name + "'")
    columns = create_column_definitions_from_file(name)
    columns = sanitize_column_definitions(columns)
    table_name = "dbpedia_" + os.path.basename(name.replace(".json.gz", "")).lower()
    create_statements, drop_statements, columns = process_columns_for_relationship_tables(create_statements, drop_statements, columns, table_name)
    create_statements, alter_statements, drop_statements = create_statements_from_column_definitions(columns, table_name, create_statements, alter_statements, drop_statements)
    return create_statements, alter_statements, drop_statements

def create_column_definitions_from_file(name):
    stream = gzip.open(name)
    i = 0
    list_cnt = 0
    table_cnt = 0
    for line in stream:
        i += 1
        if (i == 1):
            json_str = line.decode("utf-8", "properties")[:-2] + '}'
            columns = process_property_definitions(json_str)
        else:
            if (i == 2):
                json_str = line.decode("utf-8", "properties")[13:-2]
            else:
                json_str = line.decode("utf-8", "properties")[:-2]
            columns, list_cnt, table_cnt = process_instance(json_str, columns, list_cnt, table_cnt)
            
            if (i % 1000 == 0):
                print(i, end='\r')

            # if (i > 1000):
            #     break
    return columns

def sanitize_column_definitions(columns):
    column_names = []
    for index, column in enumerate(columns):
        label = column[1]
        if (label == "order"):
            label = "\"" + label + "\""
        else:
            try:
                int(label[0])
                label = "_" + label
            except:
                pass
        original_label = label
        j = 2
        while (label in column_names):
            label = original_label + str(j)
            j +=1
        column_names.append(label)
        columns[index][1] = label
    return columns

def process_columns_for_relationship_tables(create_statements, drop_statements, columns, table_name):
    new_columns = []
    remove_indices = []
    for index, column in enumerate(columns):
        if (column[5]):
            write_to_configuration_file(table_name[8:] + "." + column[0] + "," + table_name + "_" + column[1] + "." + column[1] + ",1")
            drop_table_statement = "DROP TABLE IF EXISTS " + table_name + "_" + column[1] + " CASCADE;"
            drop_statements.insert(0, drop_table_statement)
            create_relation_statement = "CREATE TABLE " + table_name + "_" + column[1] + " (\n        " + table_name[8:]
            create_relation_statement += " TEXT REFERENCES " + table_name + ",\n" + "        " + column[1]
            create_relation_statement += " " + column[2] + " REFERENCES dbpedia_" + column[3]
            try:
                label_index = [c[1] for c in columns].index(column[1] + "_label")
                create_relation_statement += ",\n        " + column[1] + "_label TEXT"
                remove_indices.add(label_index)
                if (columns[label_index] in new_columns):
                    new_columns.remove(columns[label_index])
            except:
                pass
            create_relation_statement += ",\n        PRIMARY KEY(" + table_name[8:] + ", " + column[1] + ")\n);"
            create_statements.append(create_relation_statement)
        else:
            if (not index in remove_indices):
                new_columns.append(column)

    return create_statements, drop_statements, new_columns

def create_statements_from_column_definitions(columns, table_name, create_statements, alter_statements, drop_statements):
    drop_stmt = "DROP TABLE IF EXISTS " + table_name + " CASCADE;"
    drop_statements.append(drop_stmt)
    create_stmt = "CREATE TABLE " + table_name + " (\n"
    for index, column in enumerate(columns):
        write_to_configuration_file(table_name[8:] + "." + column[0] + "," + table_name + "." + column[1] + "," + str(int(column[4])))
        column_str = column_str = "        " + column[1] + " " + column[2]
        if (column[4]):
            column_str += "[]"
        if (column[1] == "uri"):
            column_str += " PRIMARY KEY"
        if ((column[3] == "person") or (column[3] == "organisation")):
            alter_statements.append("ALTER TABLE " + table_name + " ADD CONSTRAINT " + column[1] 
                + "_fk FOREIGN KEY (" + column[1] + ") REFERENCES dbpedia_" + column[3] + ";")
        column_str = column_str + ",\n"
        create_stmt += column_str
    create_stmt = create_stmt[:-2] + "\n);"
    create_statements.insert(0, create_stmt)
    return create_statements, alter_statements, drop_statements

def process_property_definitions(json_str):
    obj = json.loads(json_str) 
    columns = []   

    with open("new_datatypes.txt", "w", encoding="UTF-8") as datatypes_file:
        for p in obj["properties"]:
            label = "".join([(s.lower() if s.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789' else '_') for s in p["propertyLabel"]])
            ontology_type = "other"
            if (p["propertyType"].startswith("http://dbpedia.org/ontology/")):
                data_type = "TEXT"
                if (p["propertyType"] == "http://dbpedia.org/ontology/Person"):
                    ontology_type = "person"
                elif (p["propertyType"] == "http://dbpedia.org/ontology/Organisation"):
                    ontology_type = "organisation"
            elif (p["propertyType"] in datatype_map):
                data_type = datatype_map[p["propertyType"]]
            else:
                print("Unknown type:  " + p["propertyType"], file=datatypes_file)
                data_type = "TEXT"
        
            if (p["propertyLabel"].endswith("_label")):
                URI = p["propertyURI"] + "_label"
            else:
                URI = p["propertyURI"]
            
            columns.append([URI, label, data_type, ontology_type, False, False])

    return columns

def process_instance(json_str, columns, list_cnt, table_cnt):
    obj = json.loads(json_str)

    for entry in obj:
        for attribute in obj[entry]:
            if (isinstance(obj[entry][attribute], list)):
                index = [c[0] for c in columns].index(attribute)
                if (not columns[index][4]):
                    list_cnt += 1
                    print("Discovered list element (" + str(list_cnt) + '):  ' + columns[index][1])
                    columns[index][4] = True
                    if ((columns[index][3] == "person") or (columns[index][3] == "organisation")):
                    #if (((columns[index][3] == "person") or (columns[index][3] == "organisation")) and (not columns[index][1].endswith("_label"))):
                        table_cnt += 1
                        print("Relationship table required (type " + columns[index][3] + ") (" + str(table_cnt) + ")")
                        columns[index][5] = True

    return columns, list_cnt, table_cnt

def clear_configuration_file():
    open("configuration.txt", "w", encoding="UTF-8")
    return

def write_to_configuration_file(str):
    with open("configuration.txt", "a", encoding="UTF-8") as configuration_file:
        print(str, file = configuration_file)
    return

def write_statements_to_file(create_statements, alter_statements, drop_statements):
    with open("ddl.txt", "w", encoding="UTF-8") as sql_file:
        for statement in drop_statements:
            print(statement + "\n", file = sql_file)        
        for statement in create_statements:
            print(statement + "\n", file = sql_file)
        for statement in alter_statements:
            print(statement + "\n", file = sql_file)
    return

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 2:
        print('You must give exactly one argument: a directory to process')
        sys.exit(1)
    process_dir(sys.argv[1])