# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
temp_user_table_drop = "DROP table IF EXISTS tmp_users"
song_table_drop = "DROP table IF EXISTS songs"
temp_song_table_drop = "DROP table IF EXISTS tmp_songs"
artist_table_drop = "DROP table IF EXISTS artists"
temp_artist_table_drop = "DROP table IF EXISTS tmp_artists"
time_table_drop = "DROP table IF EXISTS time"
temp_time_table_drop = "DROP table IF EXISTS tmp_time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays \
                        (songplay_id SERIAL PRIMARY KEY, start_time timestamp NOT NULL, user_id varchar NOT NULL,\
                         level varchar, song_id varchar, artist_id varchar, session_id varchar, \
                         location varchar, user_agent varchar);
                         """)

user_table_create = ("""CREATE TABLE IF NOT EXISTS users \
                    (user_id int PRIMARY KEY, first_name varchar NOT NULL, last_name varchar NOT NULL, gender varchar, level varchar NOT NULL);
                    """)
temp_user_table_create = ("""CREATE TEMP TABLE IF NOT EXISTS tmp_users (LIKE users)""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs \
                    (song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL, year int, duration float);
                    """)
temp_song_table_create = ("""CREATE TEMP TABLE IF NOT EXISTS tmp_songs (LIKE songs)""");

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists \
                      (artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude float, longitude float);
                      """)
temp_artist_table_create = ("""CREATE TEMP TABLE IF NOT EXISTS tmp_artists (LIKE artists);""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time \
                    (start_time timestamp PRIMARY KEY, hour int NOT NULL, day int NOT NULL, week int NOT NULL, month int NOT NULL, year int NOT NULL, weekday int NOT NULL);
                    """)
temp_time_table_create = ("""CREATE TEMP TABLE IF NOT EXISTS tmp_time (LIKE time)""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, \
                                                   level, song_id, artist_id, session_id,
                                                   location, user_agent) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")

user_table_insert = ("""INSERT INTO users \
                        SELECT DISTINCT ON (user_id) * \
                        FROM tmp_users ON CONFLICT (user_id) \
                        DO UPDATE SET level = EXCLUDED.level;""")
temp_user_table_insert = ("""COPY tmp_users FROM '/home/workspace/users.csv' \
                            DELIMITER ';' CSV;""")

song_table_insert = ("""INSERT INTO songs \
                        SELECT DISTINCT ON (song_id) * \
                        FROM tmp_songs ON CONFLICT(song_id) DO NOTHING;""")
temp_song_table_insert = ("""COPY tmp_songs FROM '/home/workspace/songs.csv' \
                            DELIMITER ';' CSV;""")

artist_table_insert = ("""INSERT INTO artists \
                        SELECT DISTINCT ON (artist_id) * \
                        FROM tmp_artists ON CONFLICT(artist_id) DO NOTHING;""")
temp_artist_table_insert = ("""COPY tmp_artists FROM '/home/workspace/artists.csv' \
                            DELIMITER ';' CSV;""")

time_table_insert = ("""INSERT INTO time \
                        SELECT DISTINCT ON (start_time) * \
                        FROM tmp_time ON CONFLICT(start_time) DO NOTHING;""")
temp_time_table_insert = ("""COPY tmp_time FROM '/home/workspace/time.csv' \
                            DELIMITER ';' CSV;""")

# FIND SONGS

song_select = ("""SELECT song_id, songs.artist_id \
                  FROM songs \
                  JOIN artists ON songs.artist_id = artists.artist_id
                  WHERE title = %s
                  AND artists.name = %s
                  AND duration = %s     
              """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, temp_user_table_drop, song_table_drop, temp_song_table_drop, artist_table_drop, temp_artist_table_drop, time_table_drop, temp_time_table_drop]
files = ['/home/workspace/users.csv', '/home/workspace/songs.csv', '/home/workspace/artists.csv', '/home/workspace/time.csv']