DELETE FROM integrated.almamater WHERE ctid IN (SELECT ctid FROM (SELECT ctid, ROW_NUMBER() over (PARTITION BY person_id, university ORDER BY ctid) AS rnum FROM integrated.almamater) AS t WHERE t.rnum > 1);
DELETE FROM integrated.person_country WHERE ctid IN (SELECT ctid FROM (SELECT ctid, ROW_NUMBER() over (PARTITION BY person_id, country_id ORDER BY ctid) AS rnum FROM integrated.person_country) AS t WHERE t.rnum > 1);
DELETE FROM integrated.person_occupation WHERE ctid IN (SELECT ctid FROM (SELECT ctid, ROW_NUMBER() over (PARTITION BY person_id, occupation_id ORDER BY ctid) AS rnum FROM integrated.person_occupation) AS t WHERE t.rnum > 1);
DELETE FROM integrated.person_party WHERE ctid IN (SELECT ctid FROM (SELECT ctid, ROW_NUMBER() over (PARTITION BY person_id, party_id ORDER BY ctid) AS rnum FROM integrated.person_party) AS t WHERE t.rnum > 1);