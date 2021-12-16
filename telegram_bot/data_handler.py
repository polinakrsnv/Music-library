# -*- coding: utf-8 -*-
import config
from hashlib import md5
import psycopg2

class SQLighter:
    def __init__(self, database_name='postgres'):
        #database_name = 'postgres'
        conn = psycopg2.connect(dbname=database_name, user='mlib_admin',
                                password='Password1', host='mlib.postgres.database.azure.com')
        self.connection = conn
        self.cursor = self.connection.cursor()

    def get_genre(self):
        with self.connection:
            self.cursor.execute("select genres.name from genres")
            return self.cursor.fetchall()

    def get_track_by_genre(self, genre_name):
        with self.connection:
            query = "select tracks.name, performers.name, tracks.audio_file " \
                    "from Tracks join Genres on genres.id=tracks.genre_id " \
                    "join performers on performers.id=tracks.performer_id " \
                    "where genres.name='" + str(genre_name) + "'"
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def insert_user_id(self, username, user_id, country):
        username, user_id, country = str(username), str(user_id), str(country)
        with self.connection:
            query = "insert into Users values (" + user_id + ", '" + username + "', " + country + ");"
            self.cursor.execute(query)

    def get_track_by_name(self, track_name):
        track_name = str(track_name)
        with self.connection:
            #print(track_name)
            query = "select tracks.name, performers.name, tracks.audio_file " \
                    "from Tracks join performers on performers.id=tracks.performer_id " \
                    "where tracks.name like '%" + track_name + "%'"
            #query2 = "SELECT tracks.id FROM Tracks where tracks.name like '%" + track_name + "%'"
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def return_track_id(self, track_name):
        track_name = str(track_name)
        with self.connection:
            #print(track_name)
            query = "select tracks.id from Tracks where tracks.name like '%" + track_name + "%'"
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def insert_playlist(self, track_id, user_id):
        track_id = str(track_id)
        user_id = str(user_id)
        with self.connection:
            #print(track_id)
            query = "insert into Playlist values (" + track_id + "," + user_id + ");"
            self.cursor.execute(query)

    def get_top_3(self, country):
        country = str(country)
        with self.connection:
            query = "with count_tracks as (select count(*) as count_, playlist.track_id as track_id " \
                    "from playlist " \
                    "group by playlist.track_id " \
                    "order by count(*) desc limit 3) " \
                    "select count_tracks.count_, tracks.name, performers.name, tracks.audio_file " \
                    "from playlist join tracks on tracks.id = playlist.track_id " \
                    "join users on playlist.user_id = users.id " \
                    "join countries on users.country_id = countries.id " \
                    "join performers on tracks.performer_id = performers.id " \
                    "join count_tracks on count_tracks.track_id = playlist.track_id " \
                    "where country_id = " + country + " and playlist.track_id in (count_tracks.track_id) " \
                                                      "group by tracks.name, count_tracks.count_, performers.name, tracks.audio_file " \
                                                      "order by count_tracks.count_ desc"

            self.cursor.execute(query)
            return self.cursor.fetchall()

    def get_top_3_artists(self, country):
        country = str(country)
        with self.connection:
            query = "with count_tracks as (select count(*) as count_, performers.id as track_id " \
                    "from playlist join tracks on playlist.track_id = tracks.id " \
                    "join performers on performers.id = tracks.performer_id " \
                    "group by performers.id " \
                    "order by count(*) desc limit 3) " \
                    "select count_tracks.count_, tracks.name, performers.name " \
                    "from playlist join tracks on tracks.id = playlist.track_id " \
                    "join users on playlist.user_id = users.id " \
                    "join countries on users.country_id = countries.id " \
                    "join performers on tracks.performer_id = performers.id " \
                    "join count_tracks on count_tracks.track_id = performers.id " \
                    "where country_id = " + country + " and performers.id in(count_tracks.track_id) " \
                    "group by tracks.name, count_tracks.count_, performers.name " \
                                                      "order by count_tracks.count_ desc"
            self.cursor.execute(query)
            return self.cursor.fetchall()

    def get_top_3_albums(self, country):
        country = str(country)
        with self.connection:
            query = "with count_tracks as (select count(*) as count_, albums.id as track_id " \
                    "from playlist join tracks on playlist.track_id = tracks.id " \
                    "join albums on albums.id = tracks.album_id " \
                    "group by albums.id " \
                    "order by count(*) desc limit 3) " \
                    "select albums.name " \
                    "from playlist join tracks on tracks.id = playlist.track_id " \
                    "join users on playlist.user_id = users.id " \
                    "join countries on users.country_id = countries.id " \
                    "join performers on tracks.performer_id = performers.id " \
                    "join albums on albums.performer_id = performers.id " \
                    "join count_tracks on count_tracks.track_id = albums.id " \
                    "where country_id = " + country + " and albums.id in(count_tracks.track_id) " \
                                                      "group by tracks.name, count_tracks.count_, albums.name " \
                                                      "order by count_tracks.count_ desc "
        self.cursor.execute(query)
        return self.cursor.fetchall()

