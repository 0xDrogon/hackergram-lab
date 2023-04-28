DROP DATABASE IF EXISTS hackergramdb;
CREATE DATABASE hackergramdb;

DROP USER IF EXISTS 'hackergram'@'localhost';
DROP USER IF EXISTS 'hackergram'@'%';
CREATE USER 'hackergram'@'localhost' IDENTIFIED BY 'hackergrampass';
CREATE USER 'hackergram'@'%' IDENTIFIED BY 'hackergrampass';

GRANT ALL PRIVILEGES ON hackergramdb.* TO 'hackergram'@'localhost';
GRANT ALL PRIVILEGES ON hackergramdb.* TO 'hackergram'@'%';

USE hackergramdb;

CREATE TABLE Users ( 
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL, 
    name TEXT,
    bio TEXT, 
    photo varchar(255) DEFAULT 'default.jpg',
    PRIMARY KEY (username)
);
CREATE TABLE Posts ( 
    id int(11) NOT NULL AUTO_INCREMENT,
    author VARCHAR(20) NOT NULL,
    content TEXT,
    posted_at timestamp default now() ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (author) REFERENCES Users(username)
);
CREATE TABLE Friends ( 
    id int(11) NOT NULL AUTO_INCREMENT,
    username1 VARCHAR(20) NOT NULL,
    username2 VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username1) REFERENCES Users(username),
    FOREIGN KEY (username2) REFERENCES Users(username)
);
CREATE TABLE Requests ( 
    id int(11) NOT NULL AUTO_INCREMENT,
    username1 VARCHAR(20) NOT NULL, 
    username2 VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username1) REFERENCES Users(username),
    FOREIGN KEY (username2) REFERENCES Users(username)
);

INSERT INTO Users(username, password, name, bio) VALUES ('admin', '1_4m_Th3_4dm1n', 'Administrator', 'I am the Administrator of Hackergram.');
INSERT INTO Users(username, password, name, bio, photo) VALUES ('mr_robot', 'elliot123', 'Mr. Robot', 'Control is an illusion.', 'mrrobot.png');
INSERT INTO Users(username, password, name, bio, photo) VALUES ('dpr', 'silk-road', 'Dread Pirate Roberts', '#FreeRoss', 'dpr.jpg');
INSERT INTO Users(username, password, name, bio) VALUES ('satoshi', 'bitcoin2009', 'Satoshi Nakamoto', 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks');
INSERT INTO Users(username, password, name, bio, photo) VALUES ('heisenberg', 'walter1958', 'Heisenberg', 'Say my name.', 'heisenberg.png');
INSERT INTO Users(username, password, name, bio, photo) VALUES ('rick', 'RickC-137', 'Rick Sanchez', 'Wubba lubba dub-dub!', 'rick.png');
INSERT INTO Users(username, password, name, bio, photo) VALUES ('stark', 'winterfell', 'Ned Stark', 'Winter is coming...', 'stark.jpg');
INSERT INTO Users(username, password, name) VALUES ('anon1', '1', 'Anonymous #1');
INSERT INTO Users(username, password, name) VALUES ('anon2', '2', 'Anonymous #2');
INSERT INTO Users(username, password, name) VALUES ('anon3', '3', 'Anonymous #3');

INSERT INTO Posts(author, content) VALUES ('admin', 'These walls have eyes and ears.');
INSERT INTO Posts(author, content) VALUES ('mr_robot', 'We are all living in each other''s paranoia.');
INSERT INTO Posts(author, content) VALUES ('heisenberg', 'Stay out of my territory.');
INSERT INTO Posts(author, content) VALUES ('dpr', 'Every action you take outside the scope of government control strengthens the market and weakens the state.');
INSERT INTO Posts(author, content) VALUES ('mr_robot', 'A bug is never just a mistake. It represents something bigger. An error of thinking that makes you who you are.');
INSERT INTO Posts(author, content) VALUES ('mr_robot', 'I wanted to save the world...');
INSERT INTO Posts(author, content) VALUES ('dpr', 'The state may try to ban our tools, but if we never use them for fear of them being banned, then we have already lost.');
INSERT INTO Posts(author, content) VALUES ('rick', 'To live is to risk it all; otherwise, you''re just an inert chunk of randomly assembled molecules drifting wherever the universe blows you.');
INSERT INTO Posts(author, content) VALUES ('dpr', 'The question I present to you is: Do we want a single entity monopolizing the provision of all critical goods and services, or do we want a choice?');
INSERT INTO Posts(author, content) VALUES ('satoshi', 'Lost coins only make everyone else''s coins worth slightly more. Think of it as a donation to everyone.');
INSERT INTO Posts(author, content) VALUES ('rick', 'I turned myself into a pickle, Morty!');
INSERT INTO Posts(author, content) VALUES ('stark', 'The man who passes the sentence should swing the sword.');
INSERT INTO Posts(author, content) VALUES ('heisenberg', 'I am the one who knocks!');
INSERT INTO Posts(author, content) VALUES ('satoshi', 'If you don''t believe it or don''t get it, I don''t have the time to try to convince you, sorry.');
INSERT INTO Posts(author, content) VALUES ('heisenberg', 'I won.');
INSERT INTO Posts(author, content) VALUES ('satoshi', 'Governments are good at cutting off the heads of a centrally controlled networks like Napster, but pure P2P networks like Gnutella and Tor seem to be holding their own.');
INSERT INTO Posts(author, content) VALUES ('rick', 'I''m sorry, but your opinion means very little to me.');
INSERT INTO Posts(author, content) VALUES ('stark', 'When the snows fall and the white winds blow, the lone wolf dies, but the pack survives.');

INSERT INTO Friends(username1, username2) VALUES ('mr_robot', 'dpr');
INSERT INTO Friends(username1, username2) VALUES ('mr_robot', 'satoshi');
INSERT INTO Friends(username1, username2) VALUES ('mr_robot', 'heisenberg');
INSERT INTO Friends(username1, username2) VALUES ('mr_robot', 'rick');
INSERT INTO Friends(username1, username2) VALUES ('mr_robot', 'stark');
INSERT INTO Friends(username1, username2) VALUES ('dpr', 'satoshi');
INSERT INTO Friends(username1, username2) VALUES ('heisenberg', 'satoshi');
INSERT INTO Friends(username1, username2) VALUES ('heisenberg', 'rick');
INSERT INTO Friends(username1, username2) VALUES ('satoshi', 'rick');

INSERT INTO Requests(username1, username2) VALUES ('anon1', 'mr_robot');
INSERT INTO Requests(username1, username2) VALUES ('anon2', 'mr_robot');
INSERT INTO Requests(username1, username2) VALUES ('anon3', 'mr_robot');