#! python3

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

ERROR_TABLE_EXISTS = "42P07"
ERROR_PQ_VIOLATION = "23505"

# connect do database
conn = psycopg2.connect(database='abgeordnetenwatch', user='postgres', password='dbpass')
cur = conn.cursor()

# set isolation level to allow for create statements
conn.set_isolation_level(0)

# executeSQL(cur, "DROP TABLE candidacy")
# executeSQL(cur, "DROP TABLE candidate")
# executeSQL(cur, "DROP TABLE constituency")
# executeSQL(cur, "DROP TABLE parliament")

# try to create tables, ignore exceptions if the tables exist
executeSQL(cur, 
    """CREATE TABLE parliament (uuid UUID PRIMARY KEY, name TEXT, startDate TEXT, endDate TEXT, 
    electionDate TEXT)""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE constituency (uuid UUID PRIMARY KEY, parliament UUID REFERENCES parliament, 
    name TEXT, areacodes TEXT[])""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE candidate (uuid UUID PRIMARY KEY, username TEXT, firstname TEXT, lastname TEXT, gender TEXT, 
    birthyear INT, education TEXT, profession TEXT, email TEXT, twitter TEXT, degree TEXT, country TEXT, 
    county TEXT, city TEXT, postal_code TEXT, picture_url TEXT)""", [ERROR_TABLE_EXISTS])
executeSQL(cur, 
    """CREATE TABLE candidacy (parliament UUID REFERENCES parliament, candidate UUID REFERENCES candidate, 
    constituency UUID REFERENCES constituency, party TEXT, number INT, result TEXT, won BOOLEAN,   
    PRIMARY KEY (parliament, candidate))""", [ERROR_TABLE_EXISTS])

# request all parliaments
parliaments_request = requests.get("https://www.abgeordnetenwatch.de/api/parliaments.json")
parliaments_data = json.loads(parliaments_request.text)

for p in parliaments_data["parliaments"]:

    print(p["uuid"] + "  " + p["name"])
    
    # insert parliament entry
    executeSQL(
        cur, 
        "INSERT INTO parliament (uuid, name, startDate, endDate, electionDate) VALUES (%s, %s, %s, %s, %s)",
        [ERROR_PQ_VIOLATION], 
        (p["uuid"], p["name"], p["dates"]["start"], p["dates"]["end"], p["dates"]["election"]))

    # request all constituencies for the parliament
    constituency_request = requests.get("https://www.abgeordnetenwatch.de/api/parliament/" + p["name"] + "/constituencies.json")
    constituency_data = json.loads(constituency_request.text)

    for c in constituency_data["constituencies"]:
        
        # gather area codes (exclude empty strings and large area codes [typos?])
        area_codes = []
        for area_code in c["areacodes"]:
            area_codes.append(area_code["code"])

        # insert constituency entry
        executeSQL(
            cur,
            "INSERT INTO constituency (uuid, parliament, name, areacodes) VALUES (%s, %s, %s, %s)",
            [ERROR_PQ_VIOLATION],
            (c["uuid"], p["uuid"], c["name"], area_codes))

    # retrieve all profiles for parliament
    profile_request = requests.get("https://www.abgeordnetenwatch.de/api/parliament/" + p["name"] + "/profiles.json")
    if (not profile_request.text):
        continue
    profile_data = json.loads(profile_request.text)

    for pr in profile_data["profiles"]:

        # insert candidate entry
        executeSQL(
            cur,
            """INSERT INTO candidate (uuid, username, firstname, lastname, gender, birthyear, education, profession,
            email, twitter, degree, country, county, city, postal_code, picture_url) VALUES (%s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            [ERROR_PQ_VIOLATION],
            (pr["meta"]["uuid"], pr["meta"]["username"], pr["personal"]["first_name"],
            pr["personal"]["last_name"], pr["personal"]["gender"], pr["personal"]["birthyear"],
            pr["personal"]["education"], pr["personal"]["profession"], pr["personal"]["email"],
            pr["personal"]["twitter"], pr["personal"]["degree"], pr["personal"]["location"]["country"],
            pr["personal"]["location"]["county"], pr["personal"]["location"]["city"],
            pr["personal"]["location"]["postal_code"], pr["personal"]["picture"]["url"]))
        
        # continue if there is no valid constituency entry        
        if (not "uuid" in pr["constituency"]):
            continue

        # insert consistuency entry for the rare case that it's not there already
        executeSQL(
            cur,
            "INSERT INTO constituency (uuid, parliament, name) VALUES (%s, %s, %s)",
            [ERROR_PQ_VIOLATION],
            (pr["constituency"]["uuid"], p["uuid"], pr["constituency"]["name"]))

        # insert aggregated data for candidacy
        executeSQL(
            cur,
            "INSERT INTO candidacy (parliament, candidate, constituency, party, number, result, won) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [ERROR_PQ_VIOLATION],
            (p["uuid"], pr["meta"]["uuid"], pr["constituency"]["uuid"], pr["party"], 
            pr["constituency"]["number"], pr["constituency"]["result"], pr["constituency"]["won"]))

print("\nsuccess")