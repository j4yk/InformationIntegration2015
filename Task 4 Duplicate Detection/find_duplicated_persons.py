#! python3 

# psql -d dbname -t -A -F"," -c "select * from users" > output.csv postgres

# from python examples
import unicodecsv as csv

def import_from_csv(name):
    with open(name,  'rb') as csvfile:
        csvreader = csv.reader(csvfile, encoding='utf-8', delimiter=',', quotechar='|')
        data = []
        for row in csvreader:
            data.append(row)
    return data

# from wikipedia
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def compare(row1, row2, d):
    # first and last_name, birth and death year 
    try:
        if (levenshtein(row1[1], row2[1]) < 2
            and levenshtein(row1[2], row2[2]) < 2
            and (row1[3]=="" or row2[3]=="" or abs(int(row1[3]) - int(row2[3])) < 5)
            and (row1[6]=="" or row2[6]=="" or abs(int(row1[6]) - int(row2[6])) < 5)):
            print([row1[0], row2[0]])
    except ValueError:
        # year wasn't a int
        pass
    except IndexError:        
        pass

data = import_from_csv('person_birth_death.csv')

# sort using lastName
data = sorted(data, key=lambda person: person[1])

duplicates = []
for i, row in enumerate(data):
    if (i%3 != 0):
        continue
    # no name
    if row[1] == "" and row[2] == "":
        continue
    compare(row, data[i+1], duplicates)
    compare(row, data[i+2], duplicates)
    compare(data[i+1], data[i+2])

#print("Found", len(duplicates), "duplicates!")
print(duplicates)
