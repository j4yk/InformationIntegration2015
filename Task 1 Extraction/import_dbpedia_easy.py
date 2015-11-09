#! python3
# -*- coding: utf-8 -*-

import psycopg2
import requests
import json

# try to execute SQL and swallow exceptions for specified error codes
def executeSQL(cur, sql, ignoreCodes = [], params = () ):
    try:
        cur.execute(sql, params)
    except psycopg2.Error as e:
        if (e.pgcode not in ignoreCodes):
            print("error code: " + e.pgcode)
            raise
    return

PERSON_LINK = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0ASELECT+DISTINCT%3Fperson+%3Ffirstname+%3Flastname+%3FbirthDate%0D%0AFROM+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0AWHERE+%7B%0D%0A++++%3Fperson+rdf%3Atype+dbo%3APerson.%0D%0A++++%3Fperson+foaf%3AgivenName+%3Ffirstname.%0D%0A++++%3Fperson+foaf%3Asurname+%3Flastname.%0D%0A++++OPTIONAL+%7B%0D%0A++++++++%3Fperson+dbo%3AbirthDate+%3FbirthDate.%0D%0A++++++++FILTER%28DATATYPE%28%3FbirthDate%29+%3D+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23date%3E%29.%0D%0A++++%7D%0D%0A++++%3Fperson+dbo%3Aparty+%3Fparty.%0D%0A++++%3Fparty+dbp%3AnativeName+%3Fpartyname.%0D%0A%7D%0D%0AGROUP+BY+%3Fperson+%3Ffirstname+%3Flastname+%3FbirthDate%0D%0AORDER+BY+%3Fperson&output=json"
PARTY_LINK = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0ASELECT+DISTINCT+%3Fparty+min%28%3FpartyName%29+as+%3Fpartyname%0D%0AFROM+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0AWHERE+%7B%0D%0A++++%3Fperson+rdf%3Atype+dbo%3APerson.%0D%0A++++%3Fperson+foaf%3AgivenName+%3Ffirstname.%0D%0A++++%3Fperson+foaf%3Asurname+%3Flastname.%0D%0A++++%3Fperson+dbo%3AbirthDate+%3FbirthDate.%0D%0A++++%3Fperson+dbo%3Aparty+%3Fparty.%0D%0A++++%3Fparty+dbp%3AnativeName+%3FpartyName.%0D%0A%7D%0D%0AGROUP+BY+%3Fparty%0D%0AORDER+BY+%3Fparty&output=json"
UNI_LINK = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0ASELECT+DISTINCT+%3Funiversity+min%28%3FuniversityName%29+as+%3Funiversityname%0D%0AFROM+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0AWHERE+%7B%0D%0A++++%3Fperson+rdf%3Atype+dbo%3APerson.%0D%0A++++%3Fperson+foaf%3AgivenName+%3Ffirstname.%0D%0A++++%3Fperson+foaf%3Asurname+%3Flastname.%0D%0A++++%3Fperson+dbo%3AbirthDate+%3FbirthDate.%0D%0A++++%3Fperson+dbo%3Aparty+%3Fparty.%0D%0A++++%3Fparty+dbp%3AnativeName+%3Fpartyname.%0D%0A++++%3Fperson+dbo%3AalmaMater+%3Funiversity.%0D%0A++++%3Funiversity+foaf%3Aname+%3FuniversityName.%0D%0A%7D%0D%0AGROUP+BY+%3Funiversity%0D%0AORDER+BY+%3Funiversity&output=json"
PERSON_PARTY_LINK = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0ASELECT+DISTINCT+%3Fperson+%3Fparty%0D%0AFROM+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0AWHERE+%7B%0D%0A++++%3Fperson+rdf%3Atype+dbo%3APerson.%0D%0A++++%3Fperson+foaf%3AgivenName+%3Ffirstname.%0D%0A++++%3Fperson+foaf%3Asurname+%3Flastname.%0D%0A++++%3Fperson+dbo%3AbirthDate+%3FbirthDate.%0D%0A++++%3Fperson+dbo%3Aparty+%3Fparty.%0D%0A++++%3Fparty+dbp%3AnativeName+%3Fpartyname.%0D%0A%7D%0D%0AORDER+BY+%3Fperson&output=json"
PERSON_UNI_LINK = "http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=PREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+dc%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+dbpedia2%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+dbpedia%3A+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0ASELECT+DISTINCT+%3Fperson+%3Funiversity%0D%0AFROM+%3Chttp%3A%2F%2Fdbpedia.org%2F%3E%0D%0AWHERE+%7B%0D%0A++++%3Fperson+rdf%3Atype+dbo%3APerson.%0D%0A++++%3Fperson+foaf%3AgivenName+%3Ffirstname.%0D%0A++++%3Fperson+foaf%3Asurname+%3Flastname.%0D%0A++++%3Fperson+dbo%3AbirthDate+%3FbirthDate.%0D%0A++++%3Fperson+dbo%3Aparty+%3Fparty.%0D%0A++++%3Fparty+dbp%3AnativeName+%3Fpartyname.%0D%0A++++%3Fperson+dbo%3AalmaMater+%3Funiversity.%0D%0A++++%3Funiversity+foaf%3Aname+%3FuniversityName.%0D%0A%7D%0D%0AORDER+BY+%3Fperson&output=json"

ERROR_TABLE_EXISTS = "42P07"
ERROR_PQ_VIOLATION = "23505"

# connect do database
conn = psycopg2.connect(database='informationIntegration', user='DBUser', password='Password')
cur = conn.cursor()

# set isolation level to allow for create statements
conn.set_isolation_level(0)

#executeSQL(cur, "DROP TABLE person CASCADE")
#executeSQL(cur, "DROP TABLE party CASCADE")
#executeSQL(cur, "DROP TABLE uni CASCADE")
#executeSQL(cur, "DROP TABLE person_party CASCADE")
#executeSQL(cur, "DROP TABLE person_uni CASCADE")

# try to create tables, ignore exceptions if the tables exist
executeSQL(cur, 
    """CREATE TABLE person (id TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, birthdate DATE)""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE party (party TEXT PRIMARY KEY, partyname TEXT)""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE uni (university TEXT PRIMARY KEY, universityname TEXT)""", [ERROR_TABLE_EXISTS])
## relation tables
executeSQL(cur, 
    """CREATE TABLE person_party (person TEXT references person, party TEXT references party)""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE person_uni (person TEXT references person, university TEXT references uni)""", [ERROR_TABLE_EXISTS])

# request data
person_data = json.loads(requests.get(PERSON_LINK).text)
party_data = json.loads(requests.get(PARTY_LINK).text)
uni_data = json.loads(requests.get(UNI_LINK).text)
person_party_data = json.loads(requests.get(PERSON_PARTY_LINK).text)
person_uni_data = json.loads(requests.get(PERSON_UNI_LINK).text)

for p in person_data["results"]["bindings"]:
    if "birthDate" in p: 
        date = p["birthDate"]["value"]
    else:
        date = None;

    # insert person entry
    executeSQL(
        cur, 
        "INSERT INTO person (id, firstname, lastname, birthdate) VALUES"
        + " (%s, %s, %s, %s)", [ERROR_PQ_VIOLATION], 
        (p["person"]["value"], p["firstname"]["value"], p["lastname"]["value"], date))

for p in party_data["results"]["bindings"]:
    # insert party entry
    executeSQL(
        cur, 
        "INSERT INTO party (party, partyname) VALUES"
        + " (%s, %s)", [ERROR_PQ_VIOLATION], 
        (p["party"]["value"], p["partyname"]["value"]))

for p in uni_data["results"]["bindings"]:
    # insert university entry
    executeSQL(
        cur, 
        "INSERT INTO uni (university, universityname) VALUES"
        + " (%s, %s)", [ERROR_PQ_VIOLATION], 
        (p["university"]["value"], p["universityname"]["value"]))

for p in person_party_data["results"]["bindings"]:
    # insert person_party entry
    executeSQL(
        cur, 
        "INSERT INTO person_party (person, party) VALUES"
        + " (%s, %s)", [ERROR_PQ_VIOLATION], 
        (p["person"]["value"], p["party"]["value"]))

for p in person_uni_data["results"]["bindings"]:
    # insert person_uni entry
    executeSQL(
        cur, 
        "INSERT INTO person_uni (person, university) VALUES"
        + " (%s, %s)", [ERROR_PQ_VIOLATION], 
        (p["person"]["value"], p["university"]["value"]))

print("\nsuccess")    