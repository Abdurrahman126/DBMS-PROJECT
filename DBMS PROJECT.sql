CREATE DATABASE Society_Management_system;
use Society_Management_system;
Create Table users(user_id int primary key, email varchar(50) unique not null, password varchar(25) not null,position varchar(20) not null);
create table announcements(announcement_id int primary key, announcement_title varchar(50) not null, content varchar(500) not null);
create table inductions(induction_id int primary key, applicant_id int, foreign key (applicant_id) references users(user_id),applying_for varchar(20) not null);
create table members(member_id int primary key,member_name varchar(30) not null, member_user_id int ,foreign key(member_user_id) references users(user_id),appointed_as varchar(20) not null);
create table society_events(event_id int primary key,  event_title varchar(100) not null, about_event varchar(500) not null, event_date date not null,venue varchar(20) not null);
create table accounts(account_id int primary key, account_balance int not null, budget int not null);
create table attendance(attendance_id int primary key, user_id int,foreign key(user_id) references users(user_id), event_id int, foreign key (event_id) references society_events(event_id),was_present boolean not null);
create table achievements(achievement_id int primary key,user_id int,foreign key(user_id) references users(user_id),achievement_title varchar(20) not null,description varchar(500) not null,date_of_achievement date not null);
create table feedback(feedback_id int primary key,user_id int,foreign key(user_id) references users(user_id),feedback_content varchar(500) not null,submitted_at timestamp default current_timestamp not null);
create table participants(participant_id int primary key,user_id int, foreign key(user_id) references users(user_id), competition_id int, foreign key(competition_id) references society_events(event_id), paricipant_name varchar(50) not null);
create table mentor(mentor_id int primary key, mentor_user_id int, foreign key(mentor_user_id) references users(user_id),mentor_name varchar(30) not null,mentor_email varchar(50) not null unique);
create table certifications(certification_id int primary key, participant_id int, foreign key(participant_id) references participants(participant_id), person_name varchar(30) not null);


