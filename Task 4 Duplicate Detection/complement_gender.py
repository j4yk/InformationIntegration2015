#! python3

import re
import sys
import pg8000
from sqlutils import fix_broken_umlauts

pattern_ends_with_frau = re.compile('[Ff]rau$')
pattern_ends_with_tin_or_rin = re.compile('[tr]in$')
pattern_contains_weiblich = re.compile('[Ww]eiblich')

def main():
    if len(sys.argv) != 4:
        print('Invalid cmd params. Usage: database username password')
        return

    conn = pg8000.connect(database=sys.argv[1], user=sys.argv[2], password=sys.argv[3])
    cur = conn.cursor()

    with open('output_correct_genders.txt', 'w', encoding='utf-8') as f:
        cur.execute("""
            SELECT person.id, gender, label FROM 
                integrated.person
                JOIN integrated.person_occupation AS po ON person.id = po.person_id
                JOIN integrated.occupation on occupation.id = po.occupation_id
            """)
        for row in cur.fetchall():
            occupation = fix_broken_umlauts(row[2])
            if pattern_ends_with_tin_or_rin.search(occupation) \
                or pattern_ends_with_frau.search(occupation) \
                or pattern_contains_weiblich.search(occupation):
                    if row[1] != 'f':
                        f.write("UPDATE integrated.person SET gender = 'f' WHERE id = %i;\n" % row[0])

if __name__ == '__main__':
    main()
