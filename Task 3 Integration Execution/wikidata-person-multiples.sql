-- no multiple genders!

-- multiple birthplaces:
select distinct id, name from person group by id, name, occupation, country, born, died, gender having(count(distinct birthplace)) > 1

-- multiple birthdates:
select id, name, born from (
select distinct id, name from person group by id, name, occupation, country, birthplace, died, gender having(count(distinct born)) > 1
) a join (select id as jid, born from person group by id, name, born) b on id = jid

-- multiple deathdates
select distinct id, name from person group by id, name, occupation, country,born,birthplace,gender having(count(distinct died)) > 1

-- multiple names
select mn.id, p.name from (select distinct id from person group by id,occupation,country,born,birthplace,died,gender having(count(distinct name)) > 1) mn
join (select id, name from person group by id, name) p on p.id = mn.id

-- multiple countries
select distinct id, name from person group by id, name, occupation,born,birthplace,died,gender having(count(distinct country)) > 1

-- multiple occupations
select distinct id, name from person group by id, name,country,born,birthplace,died,gender having(count(distinct occupation)) > 1



select name, died, to_timestamp(cast(trim(leading 't' from died) as integer)) from person where died not like '____-__-__T__:__:__Z'

select name, born, to_timestamp(cast(trim(leading 't' from born) as integer)) from person where born not like '____-__-__T__:__:__Z'