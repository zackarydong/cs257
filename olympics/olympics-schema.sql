CREATE TABLE athletes (
     id SERIAL,
     firstname text,
     nickname text,
     lastname text,
     gender text,
     team text
);

CREATE TABLE event_categories (
     id SERIAL,
     name text
);

CREATE TABLE events (
     id SERIAL,
     event_category_id int,
     event text
);

CREATE TABLE games (
     id SERIAL,
     year int,
     season text,
     city text
);

CREATE TABLE regions (
     id SERIAL,
     noc text,
     country text,
     notes text
);

CREATE TABLE event_results (
     athlete_id int,
     event_id int,
     games_id int,
     regions_id int,
     medal text
);
