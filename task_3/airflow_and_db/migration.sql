create user ya_practicum with password 'ya_practicum';

create database ya_practicum_db;

grant all privileges on database "ya_practicum_db" to ya_practicum;

\connect ya_practicum_db;

set role ya_practicum;

create schema sandbox;

create table sandbox.exchange_rate(
exchange_dt timestamptz not null,
currency_pair varchar(6) not null,
rate numeric not null
);
