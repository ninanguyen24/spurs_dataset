CREATE TABLE games (
    gameid VARCHAR(255) NOT NULL,
    gamedate DATE NOT NULL,
    PRIMARY KEY (gameid)
);

CREATE TABLE events (
    eventid INT NOT NULL,
    gameid VARCHAR(255) NOT NULL,
    visitor_id INT NOT NULL,
    home_id INT NOT NULL,
    FOREIGN KEY (visitor_id) REFERENCES teams(teamid),
    FOREIGN KEY (home_id) REFERENCES teams(teamid),
    FOREIGN KEY (gameid) REFERENCES games(gameid),
    PRIMARY KEY (eventid, gameid)
);

CREATE TABLE teams (
    teamid INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(255) NOT NULL,
    PRIMARY KEY (teamid)
);

CREATE TABLE players (
    playerid INT NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    teamid INT NOT NULL,
    jersey VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    FOREIGN KEY (teamid) REFERENCES teams(teamid),
    PRIMARY KEY (playerid)
);

CREATE TABLE moments (
    gameperiod INT NOT NULL,
    timestamp VARCHAR(255) NOT NULL,
    seconds FLOAT NOT NULL,
    shotclock FLOAT NOT NULL,
    eventid INT NOT NULL,
    gameid VARCHAR(255) NOT NULL,
    FOREIGN KEY (eventid, gameid) REFERENCES events(eventid, gameid),
    PRIMARY KEY (gameperiod, timestamp, gameid)
);

CREATE TABLE spurs.coordinates (
    teamid INT NOT NULL,
    playerid INT NOT NULL,
    x DECIMAL(8,5) NOT NULL,
    y DECIMAL(8,5) NOT NULL,
    z DECIMAL(8,5) NOT NULL,
    gameperiod INT NOT NULL,
    timestamp VARCHAR(255) NOT NULL,
    gameid VARCHAR(255) NOT NULL,
    FOREIGN KEY (gameid) REFERENCES games(gameid),
    FOREIGN KEY (teamid) REFERENCES teams(teamid),
    FOREIGN KEY (playerid) REFERENCES players(playerid),
    FOREIGN KEY (gameperiod, timestamp) REFERENCES moments(gameperiod, timestamp),
    PRIMARY KEY (teamid, playerid, x, y, z, gameperiod, timestamp, gameid)
);
