#!/usr/bin/env python
# coding: utf-8

# In[5]:


import json
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, TIMESTAMP, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to the database
# engine = create_engine('postgresql://username:password@host:port/database')

engine = create_engine('mysql+pymysql://root:password@localhost/spurs')

# Define the models for the tables in the DDL
Base = declarative_base()

#DONE
class Game(Base):
    __tablename__ = 'games'
    gameid = Column(String, primary_key=True)
    gamedate = Column(Date)

#DONE
class Event(Base):
    __tablename__ = 'events'
    eventid = Column(String, primary_key=True)
    gameid = Column(String, ForeignKey('games.gameid'))
    visitor_id = Column(String, ForeignKey('teams.teamid'))
    home_id = Column(String, ForeignKey('teams.teamid'))

#DONE    
class Team(Base):
    __tablename__ = 'teams'
    teamid = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)

#DONE
class Player(Base):
    __tablename__ = 'players'
    playerid = Column(Integer, primary_key=True)
    lastname = Column(String)
    firstname = Column(String)
    teamid = Column(Integer)
    jersey = Column(String)
    position = Column(String)

class Moment(Base):
    __tablename__ = 'moments'
    gameperiod = Column(Integer, primary_key=True)
    timestamp = Column(String, primary_key=True)
    seconds = Column(Float)
    shotclock = Column(Float)
    eventid = Column(String, ForeignKey('events.eventid'))
    gameid = Column(String, ForeignKey('events.gameid'),primary_key=True)

class Coordinates(Base):
    __tablename__ = 'coordinates'
    teamid = Column(Integer, primary_key=True)
    playerid = Column(Integer, primary_key=True)
    x = Column(Float, primary_key=True)
    y = Column(Float, primary_key=True)
    z = Column(Float, primary_key=True)
    gameperiod = Column(Integer, primary_key=True)
    timestamp = Column(String, primary_key=True)
    gameid = Column(String, primary_key=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Open the JSON file and load the data
with open('D:\\merged_partition_content\\Desktop\\01.01.2016.CHA.at.TOR\\0021500492.json', 'r') as json_file:
    data = json.load(json_file)

# Create a Game object and add it to the session
game = session.query(Game).filter_by(gameid=data['gameid']).first()
if game is None:
    game = Game(gameid=data['gameid'], gamedate=data['gamedate'])
    session.add(game)
    session.commit()

# Iterate through the events in the JSON data
for event_data in data['events']:
    #Check if teamid is already in table
    team_visitor = session.query(Team).filter_by(teamid=event_data['visitor']['teamid']).first()
    team_home = session.query(Team).filter_by(teamid=event_data['home']['teamid']).first()
    
    #Upload to teams table
    if team_visitor is None:
        team_visitor = Team(teamid=event_data['visitor']['teamid'],name=event_data['visitor']['name'],
                abbreviation=event_data['visitor']['abbreviation'])
        session.add(team_visitor)
    if team_home is None:
        team_home = Team(teamid=event_data['home']['teamid'],name=event_data['home']['name'],
                abbreviation=event_data['home']['abbreviation'])
        session.add(team_home)
    session.commit()
    
    #Upload to events table
    event = session.query(Event).filter_by(eventid=event_data['eventId'], gameid=data['gameid']).first()
    if event is None:
        event = Event(eventid=event_data['eventId'], gameid=data['gameid'], 
                  visitor_id=event_data['visitor']['teamid'], home_id=event_data['home']['teamid'])
        session.add(event)
    session.commit()
    
    # Iterate through the players in the event data
    for player_data in event_data['visitor']['players']:
        player = session.query(Player).filter_by(playerid=player_data['playerid']).first()
        if player is None:
            player = Player(playerid=player_data['playerid'], lastname=player_data['lastname'], 
                        firstname=player_data['firstname'], teamid=event_data['visitor']['teamid'],
                        jersey=player_data['jersey'], 
                        position=player_data['position'])
            session.add(player)
        session.commit()
                            
    for player_data in event_data['home']['players']:
        player = session.query(Player).filter_by(playerid=player_data['playerid']).first()
        if player is None:
            player = Player(playerid=player_data['playerid'], lastname=player_data['lastname'], 
                        firstname=player_data['firstname'], teamid=event_data['home']['teamid'],
                        jersey=player_data['jersey'], 
                        position=player_data['position'])
            session.add(player)
        session.commit()
        
    # Iterate through moments in the event data
    for moment_data in event_data['moments']:
        moment = session.query(Moment).filter_by(gameperiod=moment_data[0], timestamp=moment_data[1], gameid=data['gameid']).first()
        if moment is None:
            moment = Moment(gameperiod=moment_data[0], timestamp=moment_data[1],
                           seconds=moment_data[2],shotclock=moment_data[3],
                           eventid=event_data['eventId'],gameid=data['gameid'])
            session.add(moment)
        session.commit()
        
        # Iterate through the x/y/z coordinates
        for coord_data in moment_data[5]:
            coord = session.query(Coordinates).filter_by(teamid=coord_data[0],playerid=coord_data[1],
                                                        x=coord_data[2],y=coord_data[3],z=coord_data[4],
                                                         gameperiod=moment_data[0],timestamp=moment_data[1],
                                                         gameid=data['gameid']).first()
            if coord is None:
                coord = Coordinates(teamid=coord_data[0], playerid=coord_data[1],x=coord_data[2],
                               y=coord_data[3], z=coord_data[4], gameperiod=moment_data[0],
                                timestamp=moment_data[1], gameid=data['gameid'])
                session.add(coord)
            session.commit()


# In[ ]:




