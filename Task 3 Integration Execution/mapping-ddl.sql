--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: mapping; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA mapping;


ALTER SCHEMA mapping OWNER TO postgres;

SET search_path = mapping, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: aw_country_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE aw_country_id (
    name character varying NOT NULL,
    id integer
);


ALTER TABLE aw_country_id OWNER TO postgres;

--
-- Name: aw_occupation_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE aw_occupation_id (
    label character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE aw_occupation_id OWNER TO postgres;

--
-- Name: aw_party_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE aw_party_id (
    name character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE aw_party_id OWNER TO postgres;

--
-- Name: aw_person_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE aw_person_id (
    aw_uuid character varying NOT NULL,
    id integer
);


ALTER TABLE aw_person_id OWNER TO postgres;

--
-- Name: bundesrat_country_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE bundesrat_country_id (
    id integer NOT NULL
);


ALTER TABLE bundesrat_country_id OWNER TO postgres;

--
-- Name: bundesrat_parliament_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE bundesrat_parliament_id (
    uuid character varying NOT NULL
);


ALTER TABLE bundesrat_parliament_id OWNER TO postgres;

--
-- Name: bundesrat_party_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE bundesrat_party_id (
    name character varying NOT NULL,
    id integer
);


ALTER TABLE bundesrat_party_id OWNER TO postgres;

--
-- Name: bundesrat_person_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE bundesrat_person_id (
    name character varying NOT NULL,
    id integer
);


ALTER TABLE bundesrat_person_id OWNER TO postgres;

--
-- Name: bundesrat_state_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE bundesrat_state_id (
    name character varying NOT NULL,
    id integer
);


ALTER TABLE bundesrat_state_id OWNER TO postgres;

--
-- Name: gnd_occupation_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE gnd_occupation_id (
    name character varying NOT NULL,
    id integer
);


ALTER TABLE gnd_occupation_id OWNER TO postgres;

--
-- Name: gnd_person_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE gnd_person_id (
    gnd_id character varying NOT NULL,
    id integer
);


ALTER TABLE gnd_person_id OWNER TO postgres;

--
-- Name: gnd_place_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE gnd_place_id (
    gnd_id character varying NOT NULL,
    id integer
);


ALTER TABLE gnd_place_id OWNER TO postgres;

--
-- Name: gnd_work_id; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE gnd_work_id (
    gnd_id character varying NOT NULL,
    id integer
);


ALTER TABLE gnd_work_id OWNER TO postgres;

--
-- Name: wikidata_occupation; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE wikidata_occupation (
    wikidata_occupation_id character varying,
    integrated_occupation_id integer NOT NULL
);


ALTER TABLE wikidata_occupation OWNER TO postgres;

--
-- Name: wikidata_person; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE wikidata_person (
    wikidata_person_id character varying,
    integrated_person_id integer NOT NULL
);


ALTER TABLE wikidata_person OWNER TO postgres;

--
-- Name: wikidata_place; Type: TABLE; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE TABLE wikidata_place (
    wikidata_place_id character varying,
    integrated_place_id integer NOT NULL
);


ALTER TABLE wikidata_place OWNER TO postgres;

--
-- Name: aw_country_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aw_country_id
    ADD CONSTRAINT aw_country_id_pkey PRIMARY KEY (name);


--
-- Name: aw_occupation_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aw_occupation_id
    ADD CONSTRAINT aw_occupation_id_pkey PRIMARY KEY (label);


--
-- Name: aw_party_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aw_party_id
    ADD CONSTRAINT aw_party_id_pkey PRIMARY KEY (name);


--
-- Name: aw_person_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY aw_person_id
    ADD CONSTRAINT aw_person_id_pkey PRIMARY KEY (aw_uuid);


--
-- Name: bundesrat_country_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bundesrat_country_id
    ADD CONSTRAINT bundesrat_country_id_pkey PRIMARY KEY (id);


--
-- Name: bundesrat_parliament_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bundesrat_parliament_id
    ADD CONSTRAINT bundesrat_parliament_id_pkey PRIMARY KEY (uuid);


--
-- Name: bundesrat_party_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bundesrat_party_id
    ADD CONSTRAINT bundesrat_party_id_pkey PRIMARY KEY (name);


--
-- Name: bundesrat_person_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bundesrat_person_id
    ADD CONSTRAINT bundesrat_person_id_pkey PRIMARY KEY (name);


--
-- Name: bundesrat_state_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY bundesrat_state_id
    ADD CONSTRAINT bundesrat_state_id_pkey PRIMARY KEY (name);


--
-- Name: gnd_occupation_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY gnd_occupation_id
    ADD CONSTRAINT gnd_occupation_id_pkey PRIMARY KEY (name);


--
-- Name: gnd_person_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY gnd_person_id
    ADD CONSTRAINT gnd_person_id_pkey PRIMARY KEY (gnd_id);


--
-- Name: gnd_place_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY gnd_place_id
    ADD CONSTRAINT gnd_place_id_pkey PRIMARY KEY (gnd_id);


--
-- Name: gnd_work_id_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY gnd_work_id
    ADD CONSTRAINT gnd_work_id_pkey PRIMARY KEY (gnd_id);


--
-- Name: wikidata_occupation_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY wikidata_occupation
    ADD CONSTRAINT wikidata_occupation_pkey PRIMARY KEY (integrated_occupation_id);


--
-- Name: wikidata_person_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY wikidata_person
    ADD CONSTRAINT wikidata_person_pkey PRIMARY KEY (integrated_person_id);


--
-- Name: wikidata_place_pkey; Type: CONSTRAINT; Schema: mapping; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY wikidata_place
    ADD CONSTRAINT wikidata_place_pkey PRIMARY KEY (integrated_place_id);


--
-- Name: fki_aw_country_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_aw_country_id_fkey ON aw_country_id USING btree (id);


--
-- Name: fki_aw_occupation_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_aw_occupation_id_fkey ON aw_occupation_id USING btree (id);


--
-- Name: fki_aw_party_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_aw_party_id_fkey ON aw_party_id USING btree (id);


--
-- Name: fki_bundesrat_party_id_fk; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_bundesrat_party_id_fk ON bundesrat_party_id USING btree (id);


--
-- Name: fki_bundesrat_person_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_bundesrat_person_id_fkey ON bundesrat_person_id USING btree (id);


--
-- Name: fki_bundesrat_state_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_bundesrat_state_id_fkey ON bundesrat_state_id USING btree (id);


--
-- Name: fki_gnd_occupation_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_gnd_occupation_id_fkey ON gnd_occupation_id USING btree (id);


--
-- Name: fki_gnd_person_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_gnd_person_id_fkey ON gnd_person_id USING btree (id);


--
-- Name: fki_gnd_place_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_gnd_place_id_fkey ON gnd_place_id USING btree (id);


--
-- Name: fki_gnd_work_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_gnd_work_id_fkey ON gnd_work_id USING btree (id);


--
-- Name: fki_mapping_aw_person_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_mapping_aw_person_id_fkey ON aw_person_id USING btree (id);


--
-- Name: aw_country_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY aw_country_id
    ADD CONSTRAINT aw_country_id_fkey FOREIGN KEY (id) REFERENCES integrated.country(id);


--
-- Name: aw_occupation_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY aw_occupation_id
    ADD CONSTRAINT aw_occupation_id_fkey FOREIGN KEY (id) REFERENCES integrated.occupation(id);


--
-- Name: aw_party_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY aw_party_id
    ADD CONSTRAINT aw_party_id_fkey FOREIGN KEY (id) REFERENCES integrated.party(id);


--
-- Name: aw_person_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY aw_person_id
    ADD CONSTRAINT aw_person_id_fkey FOREIGN KEY (id) REFERENCES integrated.person(id);


--
-- Name: bundesrat_country_id_fk; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY bundesrat_country_id
    ADD CONSTRAINT bundesrat_country_id_fk FOREIGN KEY (id) REFERENCES integrated.country(id);


--
-- Name: bundesrat_parliament_id_fk; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY bundesrat_parliament_id
    ADD CONSTRAINT bundesrat_parliament_id_fk FOREIGN KEY (uuid) REFERENCES integrated.parliament(uuid);


--
-- Name: bundesrat_party_id_fk; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY bundesrat_party_id
    ADD CONSTRAINT bundesrat_party_id_fk FOREIGN KEY (id) REFERENCES integrated.party(id);


--
-- Name: bundesrat_person_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY bundesrat_person_id
    ADD CONSTRAINT bundesrat_person_id_fkey FOREIGN KEY (id) REFERENCES integrated.person(id);


--
-- Name: bundesrat_state_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY bundesrat_state_id
    ADD CONSTRAINT bundesrat_state_id_fkey FOREIGN KEY (id) REFERENCES integrated.state(id);


--
-- Name: gnd_occupation_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY gnd_occupation_id
    ADD CONSTRAINT gnd_occupation_id_fkey FOREIGN KEY (id) REFERENCES integrated.occupation(id);


--
-- Name: gnd_person_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY gnd_person_id
    ADD CONSTRAINT gnd_person_id_fkey FOREIGN KEY (id) REFERENCES integrated.person(id);


--
-- Name: gnd_place_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY gnd_place_id
    ADD CONSTRAINT gnd_place_id_fkey FOREIGN KEY (id) REFERENCES integrated.place(id);


--
-- Name: gnd_work_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY gnd_work_id
    ADD CONSTRAINT gnd_work_id_fkey FOREIGN KEY (id) REFERENCES integrated.work(id);


--
-- Name: mapping_wd_occupation_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY wikidata_occupation
    ADD CONSTRAINT mapping_wd_occupation_id_fkey FOREIGN KEY (integrated_occupation_id) REFERENCES integrated.occupation(id);


--
-- Name: mapping_wd_person_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY wikidata_person
    ADD CONSTRAINT mapping_wd_person_id_fkey FOREIGN KEY (integrated_person_id) REFERENCES integrated.person(id);


--
-- Name: mapping_wd_place_id_fkey; Type: FK CONSTRAINT; Schema: mapping; Owner: postgres
--

ALTER TABLE ONLY wikidata_place
    ADD CONSTRAINT mapping_wd_place_id_fkey FOREIGN KEY (integrated_place_id) REFERENCES integrated.place(id);


--
-- PostgreSQL database dump complete
--

