create database lrdb;
use lrdb;
create table profiles(fname varchar(255), lname varchar(255), email varchar(255), pswd varchar(255), id int, contr_add varchar(255) not null, primary key(id));
create table land_details (id int not null, fname varchar(255), lname varchar(255), doc1 blob, doc2 blob, doc3 blob, doc4 blob, foreign key (id) references profiles(id));
alter table land_details add sell int;
desc land_details;
desc fm_profiles;
ALTER TABLE fm_profiles
  DROP PRIMARY KEY;
select * from profiles;
alter table profiles rename to fm_profiles;