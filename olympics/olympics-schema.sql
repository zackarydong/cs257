CREATE TABLE athlete (
     id SERIAL,
     name text,
     gender text,
     age int,
     team text,
);

CREATE TABLE event_categories (
     id SERIAL,
     name text
);

CREATE TABLE events (
     id SERIAL,
     event_category_id int,
     name text
);

CREATE TABLE games (
     id SERIAL,
     year int,
     season text,
     city text,
);

CREATE TABLE linkingtable (
     athlete_id int,
     event_id int,
     games_id int,
     medal text
);
