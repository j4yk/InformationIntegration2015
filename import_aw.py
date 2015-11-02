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

# convert string from json to None if invalid
def get_str(str):
    if (str == ""):
        return None
    else:
        return str

# try to convert str from json to int
def get_int(str):
    if ((not str) or (not str.isdigit())):
        return None
    else:
        return int(str)

# try to convert str from json to float
def get_float(str):
    if ((str == "k.A.") or (not str)):
        return None
    else:
        return float(str.replace(",", "."))

# connect do database
conn = psycopg2.connect(database='abgeordnetenwatch', user='postgres', password='dbpass')
cur = conn.cursor()

# set isolation level to allow for create statements
conn.set_isolation_level(0)

# try to create tables, ignore exceptions if they exist
executeSQL(cur, 
    """CREATE TABLE parliament (uuid UUID PRIMARY KEY, name TEXT, startDate DATE, endDate DATE, 
    electionDate DATE)""", ["42P07"])
executeSQL(cur, 
    """CREATE TABLE constituency (uuid UUID PRIMARY KEY, parliament UUID REFERENCES parliament, 
    name TEXT, areacodes INT[])""", ["42P07"])
executeSQL(cur, 
    """CREATE TABLE candidate (uuid UUID PRIMARY KEY, username TEXT, firstname TEXT, lastname TEXT, gender TEXT, 
    birthyear INT, education TEXT, profession TEXT, email TEXT, twitter TEXT, degree TEXT, country TEXT, 
    county TEXT, city TEXT, postal_code INT, picture_url TEXT)""", ["42P07"])
executeSQL(cur, 
    """CREATE TABLE candidacy (parliament UUID REFERENCES parliament, candidate UUID REFERENCES candidate, 
    constituency UUID REFERENCES constituency, party TEXT, num INT, result REAL,  
    PRIMARY KEY (parliament, candidate))""", ["42P07"])

# request all parliaments
parliaments_request = requests.get("https://www.abgeordnetenwatch.de/api/parliaments.json")
parliaments_data = json.loads(parliaments_request.text)

for p in parliaments_data["parliaments"]:

    print(p["uuid"] + "  " + p["name"])
    
    # insert parliament entry
    executeSQL(
        cur, 
        "INSERT INTO parliament (uuid, name, startDate, endDate, electionDate) VALUES (%s, %s, %s, %s, %s)",
        ["23505"], 
        (p["uuid"], p["name"], get_str(p["dates"]["start"]), get_str(p["dates"]["end"]), get_str(p["dates"]["election"])))

    # request all constituencies for the parliament
    constituency_request = requests.get("https://www.abgeordnetenwatch.de/api/parliament/" + p["name"] + "/constituencies.json")
    constituency_data = json.loads(constituency_request.text)

    for c in constituency_data["constituencies"]:
        
        # gather area codes (exclude empty strings and large area codes [typos?])
        area_codes = []
        for area_code in c["areacodes"]:
            if ((area_code["code"].isdigit()) and (len(area_code["code"]) < 7)):
                area_codes.append(int(area_code["code"]))

        # insert constituency entry
        executeSQL(
            cur,
            "INSERT INTO constituency (uuid, parliament, name, areacodes) VALUES (%s, %s, %s, %s)",
            ["23505"],
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
            ["23505"],
            (pr["meta"]["uuid"], get_str(pr["meta"]["username"]), get_str(pr["personal"]["first_name"]),
            get_str(pr["personal"]["last_name"]), get_str(pr["personal"]["gender"]), get_int(pr["personal"]["birthyear"]),
            get_str(pr["personal"]["education"]), get_str(pr["personal"]["profession"]), get_str(pr["personal"]["email"]),
            get_str(pr["personal"]["twitter"]), get_str(pr["personal"]["degree"]), get_str(pr["personal"]["location"]["country"]),
            get_str(pr["personal"]["location"]["county"]), get_str(pr["personal"]["location"]["city"]),
            get_int(pr["personal"]["location"]["postal_code"]), get_str(pr["personal"]["picture"]["url"])))
        
        # continue if there is no valid constituency entry        
        if (not "uuid" in pr["constituency"]):
            continue

        # insert consistuency entry for the rare case that it's not there already
        executeSQL(
            cur,
            "INSERT INTO constituency (uuid, parliament, name) VALUES (%s, %s, %s)",
            ["23505"],
            (pr["constituency"]["uuid"], p["uuid"], pr["constituency"]["name"]))

        # insert aggregated data for candidacy
        executeSQL(
            cur,
            "INSERT INTO candidacy (parliament, candidate, constituency, party, num, result) VALUES (%s, %s, %s, %s, %s, %s)",
            ["23505"],
            (p["uuid"], pr["meta"]["uuid"], pr["constituency"]["uuid"], get_str(pr["party"]), 
            get_int(pr["constituency"]["number"]), get_float(pr["constituency"]["result"])))

print("\nsuccess")