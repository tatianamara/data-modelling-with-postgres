import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def insert_data(cur, conn, create_sql, insert_temp_table, insert_table):
    '''
    Create a temporary table to store the data, insert data from the csv file into the temporary table, and insert distinct data into the original table. 
    Args:
        cur: database cursor.
        conn: database connection
        create_sql: create sql querie from sql_queries to create temp table
        insert_temp_table: insert sql querie from sql_queries to insert data into the temporary table
        insert_table: insert sql querie from sql_queries to insert distinct data into the original table
    '''
    # create tmp table
    cur.execute(create_sql)
    conn.commit()
    
    # insert data from csv file in temp table
    cur.execute(insert_temp_table)
    conn.commit()    
    
    # insert distinct data from tmp table into table
    cur.execute(insert_table)
    conn.commit()  

def process_song_file(cur, filepath):

    '''
    Reads the json file, process and convert to csv files with the right fields from song and artist df. 
    Args:
        cur: database cursor.
        filepath: filepath to the json file
    '''
    # open song file
    df = pd.read_json(filepath, lines=True)

    # create song csv file
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    
    song_data.to_csv('songs.csv', mode='a', header=False, sep=";", index=False)    
    
    # create artist csv file
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    
    artist_data.to_csv('artists.csv', mode='a', header=False, sep=";", index=False)  
    
def process_log_file(cur, filepath):

    '''
    Reads the json file, process, extract the data fields from the timestamp, and insert the right fields in the time, users and songplay tables. 
    Args:
        cur: database cursor.
        filepath: filepath to the json file
    '''
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action (valid plays where length of play is not None)
    df = df[df.page=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],  unit='ms')
    
    # convert time data to csv file
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.dayofweek]
    column_labels = ['ts', 'hour', 'day', 'week', 'month', 'year', 'dayofweek']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    
    time_df.to_csv('time.csv', mode='a', header=False, sep=";", index=False) 
    
    # convert user data to csv file
    user_df = pd.DataFrame(df, columns=('userId', 'firstName', 'lastName', 'gender', 'level'))

    user_df.to_csv('users.csv', mode='a', header=False, sep=";", index=False) 
    
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):

    '''
    Reads the json file, process, extract the data fields from the timestamp, and insert the right fields in the time, users and songplay tables. 
    Args:
        cur: database cursor.
        conn: database cunnection.
        filepath: filepath to the song_data/log_data files
        func: process_song_file or process_log_file functions.
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    
    """    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Process data to song_data file.  
    
    - Insert data into songs table
    
    - Insert data into artists table
    
    - Process data to log_data file. 
    
    - Insert data into time table
    
    - Insert data into users table
    
    - Finally, closes the connection. 
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    # process song and artist data
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    
    # insert song data
    insert_data(cur, conn, temp_song_table_create, temp_song_table_insert, song_table_insert)
      
    # insert artist data
    insert_data(cur, conn, temp_artist_table_create, temp_artist_table_insert, artist_table_insert)
    
    # process time and user data
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    
    # insert time data
    insert_data(cur, conn, temp_time_table_create, temp_time_table_insert, time_table_insert)
    
    # insert user data
    insert_data(cur, conn, temp_user_table_create, temp_user_table_insert, user_table_insert)

    conn.close()


if __name__ == "__main__":
    main()