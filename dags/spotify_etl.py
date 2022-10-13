# Import the Libaries we need to process the data and build the pipeline

import sqlalchemy
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import pandas as pd
import sqlite3
from refreshtoken import Refresh

from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook


#Checking Our Pipeline
def check_if_valid_data(df: pd.DataFrame) -> bool:
    #check if dataframe is empty (if we haven't used spotify during that day)
    if df.empty:
        print("No songs found, terminating execution")
        return False

    #Primary Key is going to be our played at because we can only play one song at a time .
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key has a duplicate")
    
    #Check for nulls 
    if   df.isnull().values.any():
        raise Exception("Null Valued found")



def  run_spotify_etl():
# Extract part of the ETL

    test = Refresh()
    test.refresh_token
    database_location = "sqlite:////usr/local/airflow/db/airflow.db"
    user_id = "11125726624"
    token = test.refresh()
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=token)
    }

    # Want time in unix milliseconds to convert yesterday date to this. Allows us to see what songs are played in the last 24 hours
    today = datetime.datetime.now()
    yesterday =  today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = headers) 

    data = r.json()

    artist_name = []
    song_name = []
    popularity = []
    release_date = []
    played_at_list =[]
    timestamps = []
    
    # Now Extract only the relevant sections within the JSON object
    for song in data["items"]:
        song_name.append(song["track"]["name"])
        artist_name.append(song["track"]["album"]["artists"][0]["name"])
        popularity.append(song["track"]["popularity"])
        release_date.append(song["track"]["album"]["release_date"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # Next Prepare the dictionary sections to turn our data into a pandas dataframe
    spotifydata = {
        "song_name": song_name,
        "artist_name": artist_name,
        "popularity": popularity,
        "release_date": release_date,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    spotify_df = pd.DataFrame(spotifydata, columns = ["song_name", "artist_name", "popularity", "release_date","played_at" ,"timestamp"])

    # Validate
    print("Validating data")
    if check_if_valid_data(spotify_df):
        print("Data is all good, proceed to Loading Stage")
    else: 
        print("Duplicate data")



# Load part of the ETL - Setup SQLAlchamy and SQLITE for our Database
    engine = sqlalchemy.create_engine(database_location)
    conn = sqlite3.connect("played_tracks.sqlite")
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        popularity VARCHAR(200),
        release_date VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Database Successfully Opened")


    try:
        spotify_df.to_sql("played_tracks", engine, index=False , if_exists='append')
    except Exception as e:
        print("There was an issue loading the data." +str(e))
    
    conn.close()
    print("Database Closed Succesfully")
