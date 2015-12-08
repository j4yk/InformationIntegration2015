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
-- Name: fki_aw_occupation_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_aw_occupation_id_fkey ON aw_occupation_id USING btree (id);


--
-- Name: fki_aw_party_id_fkey; Type: INDEX; Schema: mapping; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_aw_party_id_fkey ON aw_party_id USING btree (id);


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

-----------------
-- wikidata stuff
-----------------

CREATE TABLE wikidata_place (
    wikidata_place_id character varying,
    integrated_place_id integer,
    primary key(integrated_place_id)
);

ALTER TABLE wikidata_place OWNER TO postgres;
alter table only wikidata_place
    add constraint mapping_wd_place_id_fkey foreign key (integrated_place_id) references integrated.place(id);


CREATE TABLE wikidata_occupation (
    wikidata_occupation_id character varying,
    integrated_occupation_id integer,
    primary key(integrated_occupation_id)
);

ALTER TABLE wikidata_occupation OWNER TO postgres;
alter table only wikidata_occupation
    add constraint mapping_wd_occupation_id_fkey foreign key (integrated_occupation_id) references integrated.occupation(id);

--
-- PostgreSQL database dump complete
--

