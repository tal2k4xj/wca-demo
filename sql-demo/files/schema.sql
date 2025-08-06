--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Ubuntu 14.17-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 15.4

-- Started on 2025-03-25 09:23:47 CDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3424 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 27985)
-- Name: SequelizeMeta; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public."SequelizeMeta" (
    name character varying(255) NOT NULL
);


ALTER TABLE public."SequelizeMeta" OWNER TO locationapi;

--
-- TOC entry 212 (class 1259 OID 27999)
-- Name: city; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.city (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    override_name character varying(100),
    capital character varying(100),
    iso2 character(2) NOT NULL,
    iso3 character(3) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    population bigint,
    ranking integer,
    division_id character varying(6),
    density double precision
);


ALTER TABLE public.city OWNER TO locationapi;

--
-- TOC entry 211 (class 1259 OID 27990)
-- Name: country; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.country (
    id integer NOT NULL,
    iso2 character varying(2) NOT NULL,
    iso3 character varying(3) NOT NULL,
    name character varying(60) NOT NULL,
    show_division boolean,
    has_rail boolean
);


ALTER TABLE public.country OWNER TO locationapi;

--
-- TOC entry 215 (class 1259 OID 28034)
-- Name: country_division; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.country_division (
    id character varying(6) NOT NULL,
    iso2 character(2) NOT NULL,
    name character varying(70) NOT NULL
);


ALTER TABLE public.country_division OWNER TO locationapi;

--
-- TOC entry 217 (class 1259 OID 28157)
-- Name: city_search; Type: MATERIALIZED VIEW; Schema: public; Owner: locationapi
--

CREATE MATERIALIZED VIEW public.city_search AS
 SELECT city.id,
    (((((city.name)::text || ', '::text) || (country_division.name)::text) || ', '::text) || (country.name)::text) AS display_name,
    city.ranking,
    city.population,
    city.density,
    to_tsvector('simple'::regconfig, (((((city.name)::text || ', '::text) || (country_division.name)::text) || ', '::text) || (country.name)::text)) AS tokens
   FROM ((public.city
     JOIN public.country ON ((city.iso3 = (country.iso3)::bpchar)))
     JOIN public.country_division ON (((city.division_id)::text = (country_division.id)::text)))
  WHERE ((country.show_division = true) AND (country_division.name IS NOT NULL))
UNION
 SELECT city.id,
    (((city.name)::text || ', '::text) || (country.name)::text) AS display_name,
    city.ranking,
    city.population,
    city.density,
    to_tsvector('simple'::regconfig, (((city.name)::text || ', '::text) || (country.name)::text)) AS tokens
   FROM (public.city
     JOIN public.country ON ((city.iso3 = (country.iso3)::bpchar)))
  WHERE ((country.show_division = true) AND (city.division_id IS NULL))
UNION
 SELECT city.id,
    (((city.name)::text || ', '::text) || (country.name)::text) AS display_name,
    city.ranking,
    city.population,
    city.density,
    to_tsvector('simple'::regconfig, (((city.name)::text || ', '::text) || (country.name)::text)) AS tokens
   FROM (public.city
     JOIN public.country ON ((city.iso3 = (country.iso3)::bpchar)))
  WHERE ((country.show_division IS NULL) OR (country.show_division = false))
  ORDER BY 2, 3, 4 DESC NULLS LAST, 5 DESC NULLS LAST
  WITH NO DATA;


ALTER TABLE public.city_search OWNER TO locationapi;

--
-- TOC entry 214 (class 1259 OID 28019)
-- Name: country_currency; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.country_currency (
    country_id bigint NOT NULL,
    currency_id bigint NOT NULL,
    is_default boolean
);


ALTER TABLE public.country_currency OWNER TO locationapi;

--
-- TOC entry 216 (class 1259 OID 28060)
-- Name: country_division_subdivision; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.country_division_subdivision (
    id character varying(6) NOT NULL,
    iso2 character(2) NOT NULL,
    division_id character(6) NOT NULL,
    name character varying(70) NOT NULL
);


ALTER TABLE public.country_division_subdivision OWNER TO locationapi;

--
-- TOC entry 213 (class 1259 OID 28014)
-- Name: currency; Type: TABLE; Schema: public; Owner: locationapi
--

CREATE TABLE public.currency (
    id bigint NOT NULL,
    alpha_code character varying(3) NOT NULL,
    name character varying(100) NOT NULL,
    decimal_digits integer NOT NULL,
    flag_code character varying(10)
);


ALTER TABLE public.currency OWNER TO locationapi;

--
-- TOC entry 3248 (class 2606 OID 27989)
-- Name: SequelizeMeta SequelizeMeta_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public."SequelizeMeta"
    ADD CONSTRAINT "SequelizeMeta_pkey" PRIMARY KEY (name);


--
-- TOC entry 3258 (class 2606 OID 28003)
-- Name: city city_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (id);


--
-- TOC entry 3263 (class 2606 OID 28023)
-- Name: country_currency country_currency_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_currency
    ADD CONSTRAINT country_currency_pkey PRIMARY KEY (country_id, currency_id);


--
-- TOC entry 3265 (class 2606 OID 28038)
-- Name: country_division country_division_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_division
    ADD CONSTRAINT country_division_pkey PRIMARY KEY (id);


--
-- TOC entry 3267 (class 2606 OID 28064)
-- Name: country_division_subdivision country_division_subdivision_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_division_subdivision
    ADD CONSTRAINT country_division_subdivision_pkey PRIMARY KEY (id);


--
-- TOC entry 3250 (class 2606 OID 27996)
-- Name: country country_iso2_key; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_iso2_key UNIQUE (iso2);


--
-- TOC entry 3252 (class 2606 OID 27998)
-- Name: country country_iso3_key; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_iso3_key UNIQUE (iso3);


--
-- TOC entry 3254 (class 2606 OID 27994)
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (id);


--
-- TOC entry 3261 (class 2606 OID 28018)
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (id);


--
-- TOC entry 3259 (class 1259 OID 28057)
-- Name: ix_city_iso3; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE INDEX ix_city_iso3 ON public.city USING btree (iso3);


--
-- TOC entry 3268 (class 1259 OID 28165)
-- Name: ix_city_search_display_name; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE INDEX ix_city_search_display_name ON public.city_search USING gin (display_name public.gin_trgm_ops);


--
-- TOC entry 3269 (class 1259 OID 28164)
-- Name: ix_city_search_id; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE UNIQUE INDEX ix_city_search_id ON public.city_search USING btree (id);


--
-- TOC entry 3270 (class 1259 OID 28166)
-- Name: ix_city_search_tokens; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE INDEX ix_city_search_tokens ON public.city_search USING gin (tokens);


--
-- TOC entry 3255 (class 1259 OID 28059)
-- Name: ix_country_iso2; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE INDEX ix_country_iso2 ON public.country USING btree (iso2);


--
-- TOC entry 3256 (class 1259 OID 28058)
-- Name: ix_country_iso3; Type: INDEX; Schema: public; Owner: locationapi
--

CREATE INDEX ix_country_iso3 ON public.country USING btree (iso3);


--
-- TOC entry 3271 (class 2606 OID 28044)
-- Name: city city_division_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_division_id_fkey FOREIGN KEY (division_id) REFERENCES public.country_division(id);


--
-- TOC entry 3272 (class 2606 OID 28004)
-- Name: city city_iso2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_iso2_fkey FOREIGN KEY (iso2) REFERENCES public.country(iso2);


--
-- TOC entry 3273 (class 2606 OID 28009)
-- Name: city city_iso3_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_iso3_fkey FOREIGN KEY (iso3) REFERENCES public.country(iso3);


--
-- TOC entry 3274 (class 2606 OID 28024)
-- Name: country_currency country_currency_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_currency
    ADD CONSTRAINT country_currency_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(id);


--
-- TOC entry 3275 (class 2606 OID 28029)
-- Name: country_currency country_currency_currency_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_currency
    ADD CONSTRAINT country_currency_currency_id_fkey FOREIGN KEY (currency_id) REFERENCES public.currency(id);


--
-- TOC entry 3276 (class 2606 OID 28039)
-- Name: country_division country_division_iso2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_division
    ADD CONSTRAINT country_division_iso2_fkey FOREIGN KEY (iso2) REFERENCES public.country(iso2);


--
-- TOC entry 3277 (class 2606 OID 28070)
-- Name: country_division_subdivision country_division_subdivision_division_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_division_subdivision
    ADD CONSTRAINT country_division_subdivision_division_id_fkey FOREIGN KEY (division_id) REFERENCES public.country_division(id);


--
-- TOC entry 3278 (class 2606 OID 28065)
-- Name: country_division_subdivision country_division_subdivision_iso2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: locationapi
--

ALTER TABLE ONLY public.country_division_subdivision
    ADD CONSTRAINT country_division_subdivision_iso2_fkey FOREIGN KEY (iso2) REFERENCES public.country(iso2);


--
-- TOC entry 3425 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2025-03-25 09:23:47 CDT

--
-- PostgreSQL database dump complete
--

