--
-- PostgreSQL database dump
--

-- Dumped from database version 9.4.5
-- Dumped by pg_dump version 9.4.5
-- Started on 2015-11-18 12:26:42

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: integrated; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA integrated;


ALTER SCHEMA integrated OWNER TO postgres;

--
-- TOC entry 197 (class 3079 OID 11855)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2196 (class 0 OID 0)
-- Dependencies: 197
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = integrated, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 191 (class 1259 OID 17323)
-- Name: almamater; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE almamater (
    person_id integer,
    university character varying
);


ALTER TABLE almamater OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 17362)
-- Name: article_header; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE article_header (
    id character varying NOT NULL,
    headline character varying,
    abstract character varying,
    word_count integer,
    pub_date date,
    web_url character varying
);


ALTER TABLE article_header OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 17339)
-- Name: author; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE author (
    person_id integer NOT NULL,
    fans_count integer,
    followers_count integer,
    average_rating real,
    ratings_count integer,
    goodreads_author boolean
);


ALTER TABLE author OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 17291)
-- Name: auxiliary_income; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auxiliary_income (
    politician integer,
    type character varying,
    year integer,
    level integer,
    start_date date,
    end_date date,
    periodical character varying,
    description character varying
);


ALTER TABLE auxiliary_income OWNER TO postgres;

--
-- TOC entry 179 (class 1259 OID 17162)
-- Name: birth; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE birth (
    person_id integer,
    place_id integer,
    year integer,
    month integer,
    day integer,
    first_name character varying,
    last_name character varying
);


ALTER TABLE birth OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 17349)
-- Name: book; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE book (
    id integer NOT NULL,
    author integer,
    title character varying,
    average_rating real,
    description character varying,
    edition_information character varying,
    format character varying,
    isbd character varying,
    isbn13 character varying,
    num_pages integer,
    publication_date date,
    published integer,
    publisher character varying,
    ratings_count integer,
    text_reviews_count integer
);


ALTER TABLE book OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 17387)
-- Name: candidacy; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE candidacy (
    candidate integer NOT NULL,
    parliament character varying,
    constituency character varying,
    party_id integer,
    result real,
    num integer,
    mandate character varying,
    ended date
);


ALTER TABLE candidacy OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 17256)
-- Name: committee; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE committee (
    name character varying NOT NULL,
    url character varying,
    flyer_url character varying,
    info_text character varying
);


ALTER TABLE committee OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 17199)
-- Name: constituency; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE constituency (
    uuid character varying NOT NULL,
    name character varying,
    area_codes integer[]
);


ALTER TABLE constituency OWNER TO postgres;

--
-- TOC entry 180 (class 1259 OID 17178)
-- Name: death; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE death (
    person_id integer,
    place_id integer,
    year integer,
    month integer,
    day integer
);


ALTER TABLE death OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 17264)
-- Name: function; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE function (
    committee_name character varying,
    politician integer,
    function_name character varying
);


ALTER TABLE function OWNER TO postgres;

--
-- TOC entry 172 (class 1259 OID 17073)
-- Name: occupation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE occupation (
    id integer NOT NULL,
    label character varying
);


ALTER TABLE occupation OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 17191)
-- Name: parliament; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE parliament (
    uuid character varying NOT NULL,
    name character varying,
    start_date date,
    end_date date,
    election_date date
);


ALTER TABLE parliament OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 17207)
-- Name: party; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE party (
    id integer NOT NULL,
    uri character varying,
    name character varying
);


ALTER TABLE party OWNER TO postgres;

--
-- TOC entry 175 (class 1259 OID 17102)
-- Name: person; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person (
    id integer NOT NULL,
    first_name character varying,
    last_name character varying,
    gender character varying,
    email character varying,
    url character varying,
    twitter character varying,
    degree character varying,
    education character varying,
    dbpedia_uri character varying,
    wikidata_id character varying,
    nyt_id character varying,
    associated_articles_count integer,
    nyt_definition character varying
);


ALTER TABLE person OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 17370)
-- Name: person_article; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person_article (
    article_id character varying,
    person_id integer
);


ALTER TABLE person_article OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 17302)
-- Name: person_occupation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person_occupation (
    person_id integer,
    occupation_id integer
);


ALTER TABLE person_occupation OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 17215)
-- Name: person_party; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE person_party (
    party_id integer,
    person_id integer
);


ALTER TABLE person_party OWNER TO postgres;

--
-- TOC entry 173 (class 1259 OID 17081)
-- Name: place; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE place (
    id integer NOT NULL,
    name character varying,
    latitude real,
    longitude real,
    country character varying
);


ALTER TABLE place OWNER TO postgres;

--
-- TOC entry 176 (class 1259 OID 17115)
-- Name: politician; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE politician (
    person_id integer NOT NULL,
    aw_uuid character varying,
    aw_username character varying,
    aw_picture_url character varying,
    state character varying
);


ALTER TABLE politician OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 17280)
-- Name: position; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "position" (
    position_name character varying,
    politician integer
);


ALTER TABLE "position" OWNER TO postgres;

--
-- TOC entry 177 (class 1259 OID 17133)
-- Name: related_to; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE related_to (
    person1_id integer,
    person2_id integer,
    type character varying
);


ALTER TABLE related_to OWNER TO postgres;

--
-- TOC entry 174 (class 1259 OID 17089)
-- Name: state; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE state (
    state character varying NOT NULL,
    capital_id integer,
    area real,
    population integer
);


ALTER TABLE state OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 17315)
-- Name: university; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE university (
    uri character varying NOT NULL,
    name character varying
);


ALTER TABLE university OWNER TO postgres;

--
-- TOC entry 178 (class 1259 OID 17149)
-- Name: work; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE work (
    id integer NOT NULL,
    person_id integer,
    name character varying
);


ALTER TABLE work OWNER TO postgres;


--
-- TOC entry 2023 (class 2606 OID 17369)
-- Name: article_header_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY article_header
    ADD CONSTRAINT article_header_pkey PRIMARY KEY (id);


--
-- TOC entry 2019 (class 2606 OID 17343)
-- Name: author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY author
    ADD CONSTRAINT author_pkey PRIMARY KEY (person_id);


--
-- TOC entry 2021 (class 2606 OID 17356)
-- Name: book_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY book
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);


--
-- TOC entry 2025 (class 2606 OID 17394)
-- Name: candidacy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_pkey PRIMARY KEY (candidate, parliament, constituency);


--
-- TOC entry 2015 (class 2606 OID 17263)
-- Name: committee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY committee
    ADD CONSTRAINT committee_pkey PRIMARY KEY (name);


--
-- TOC entry 2011 (class 2606 OID 17206)
-- Name: constituency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY constituency
    ADD CONSTRAINT constituency_pkey PRIMARY KEY (uuid);


--
-- TOC entry 1997 (class 2606 OID 17080)
-- Name: occupation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY occupation
    ADD CONSTRAINT occupation_pkey PRIMARY KEY (id);


--
-- TOC entry 2009 (class 2606 OID 17198)
-- Name: parliament_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY parliament
    ADD CONSTRAINT parliament_pkey PRIMARY KEY (uuid);


--
-- TOC entry 2013 (class 2606 OID 17214)
-- Name: party_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY party
    ADD CONSTRAINT party_pkey PRIMARY KEY (id);


--
-- TOC entry 2003 (class 2606 OID 17109)
-- Name: person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- TOC entry 1999 (class 2606 OID 17088)
-- Name: place_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY place
    ADD CONSTRAINT place_pkey PRIMARY KEY (id);


--
-- TOC entry 2005 (class 2606 OID 17122)
-- Name: politician_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY politician
    ADD CONSTRAINT politician_pkey PRIMARY KEY (person_id);


--
-- TOC entry 2001 (class 2606 OID 17096)
-- Name: state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY state
    ADD CONSTRAINT state_pkey PRIMARY KEY (state);


--
-- TOC entry 2017 (class 2606 OID 17322)
-- Name: university_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY university
    ADD CONSTRAINT university_pkey PRIMARY KEY (uri);


--
-- TOC entry 2007 (class 2606 OID 17156)
-- Name: work_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY work
    ADD CONSTRAINT work_pkey PRIMARY KEY (id);


--
-- TOC entry 2045 (class 2606 OID 17329)
-- Name: almamater_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY almamater
    ADD CONSTRAINT almamater_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2046 (class 2606 OID 17334)
-- Name: almamater_university_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY almamater
    ADD CONSTRAINT almamater_university_fkey FOREIGN KEY (university) REFERENCES university(uri);


--
-- TOC entry 2047 (class 2606 OID 17344)
-- Name: author_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY author
    ADD CONSTRAINT author_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2042 (class 2606 OID 17297)
-- Name: auxiliary_income_politician_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auxiliary_income
    ADD CONSTRAINT auxiliary_income_politician_fkey FOREIGN KEY (politician) REFERENCES politician(person_id);


--
-- TOC entry 2033 (class 2606 OID 17168)
-- Name: birth_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY birth
    ADD CONSTRAINT birth_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2034 (class 2606 OID 17173)
-- Name: birth_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY birth
    ADD CONSTRAINT birth_place_id_fkey FOREIGN KEY (place_id) REFERENCES place(id);


--
-- TOC entry 2048 (class 2606 OID 17357)
-- Name: book_author_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY book
    ADD CONSTRAINT book_author_fkey FOREIGN KEY (author) REFERENCES author(person_id);


--
-- TOC entry 2051 (class 2606 OID 17395)
-- Name: candidacy_candidate_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_candidate_fkey FOREIGN KEY (candidate) REFERENCES politician(person_id);


--
-- TOC entry 2053 (class 2606 OID 17405)
-- Name: candidacy_constituency_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_constituency_fkey FOREIGN KEY (constituency) REFERENCES constituency(uuid);


--
-- TOC entry 2052 (class 2606 OID 17400)
-- Name: candidacy_parliament_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_parliament_fkey FOREIGN KEY (parliament) REFERENCES parliament(uuid);


--
-- TOC entry 2054 (class 2606 OID 17410)
-- Name: candidacy_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY candidacy
    ADD CONSTRAINT candidacy_party_id_fkey FOREIGN KEY (party_id) REFERENCES party(id);


--
-- TOC entry 2035 (class 2606 OID 17181)
-- Name: death_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY death
    ADD CONSTRAINT death_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2036 (class 2606 OID 17186)
-- Name: death_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY death
    ADD CONSTRAINT death_place_id_fkey FOREIGN KEY (place_id) REFERENCES place(id);


--
-- TOC entry 2039 (class 2606 OID 17270)
-- Name: function_committee_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY function
    ADD CONSTRAINT function_committee_name_fkey FOREIGN KEY (committee_name) REFERENCES committee(name);


--
-- TOC entry 2040 (class 2606 OID 17275)
-- Name: function_politician_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY function
    ADD CONSTRAINT function_politician_fkey FOREIGN KEY (politician) REFERENCES politician(person_id);


--
-- TOC entry 2049 (class 2606 OID 17376)
-- Name: person_article_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_article
    ADD CONSTRAINT person_article_article_id_fkey FOREIGN KEY (article_id) REFERENCES article_header(id);


--
-- TOC entry 2050 (class 2606 OID 17381)
-- Name: person_article_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_article
    ADD CONSTRAINT person_article_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);



--
-- TOC entry 2044 (class 2606 OID 17310)
-- Name: person_occupation_occupation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_occupation
    ADD CONSTRAINT person_occupation_occupation_id_fkey FOREIGN KEY (occupation_id) REFERENCES occupation(id);


--
-- TOC entry 2043 (class 2606 OID 17305)
-- Name: person_occupation_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_occupation
    ADD CONSTRAINT person_occupation_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2037 (class 2606 OID 17218)
-- Name: person_party_party_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_party
    ADD CONSTRAINT person_party_party_id_fkey FOREIGN KEY (party_id) REFERENCES party(id);


--
-- TOC entry 2038 (class 2606 OID 17223)
-- Name: person_party_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person_party
    ADD CONSTRAINT person_party_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2028 (class 2606 OID 17123)
-- Name: politician_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY politician
    ADD CONSTRAINT politician_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- TOC entry 2029 (class 2606 OID 17128)
-- Name: politician_state_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY politician
    ADD CONSTRAINT politician_state_fkey FOREIGN KEY (state) REFERENCES state(state);


--
-- TOC entry 2041 (class 2606 OID 17286)
-- Name: position_politician_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "position"
    ADD CONSTRAINT position_politician_fkey FOREIGN KEY (politician) REFERENCES politician(person_id);


--
-- TOC entry 2030 (class 2606 OID 17139)
-- Name: related_to_person1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY related_to
    ADD CONSTRAINT related_to_person1_id_fkey FOREIGN KEY (person1_id) REFERENCES person(id);


--
-- TOC entry 2031 (class 2606 OID 17144)
-- Name: related_to_person2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY related_to
    ADD CONSTRAINT related_to_person2_id_fkey FOREIGN KEY (person2_id) REFERENCES person(id);


--
-- TOC entry 2026 (class 2606 OID 17097)
-- Name: state_capital_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY state
    ADD CONSTRAINT state_capital_id_fkey FOREIGN KEY (capital_id) REFERENCES place(id);


--
-- TOC entry 2032 (class 2606 OID 17157)
-- Name: work_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY work
    ADD CONSTRAINT work_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


-- Completed on 2015-11-18 12:26:42

--
-- PostgreSQL database dump complete
--

