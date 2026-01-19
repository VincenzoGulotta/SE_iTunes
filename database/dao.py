from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def get_album(soglia):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id as album_id, a.title as title, sum(milliseconds)/60000 as minuti
                    from album a, track t
                    where a.id = t.album_id
                    group by a.id
                    having sum(milliseconds)/60000 > %s """

        cursor.execute(query,(soglia,))

        for row in cursor:
            album_id = row['album_id']
            titolo = row['title']
            minuti = float(row['minuti'])
            album = Album(album_id, titolo, minuti)
            result[album_id] = album

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni(soglia):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """ with album_validi as (
	                select a.id as album_id, a.title as title, sum(milliseconds)/60000 as minuti
	                from album a, track t
	                where a.id = t.album_id
	                group by a.id
	                having sum(milliseconds)/60000 > %s
                    )
                    select distinct pt.playlist_id as playlist_id, av.album_id as album_id
                    from album_validi av, playlist_track pt, track t
                    where t.id = pt.track_id and av.album_id = t.album_id 
                    order by pt.playlist_id """

        cursor.execute(query,(soglia,))

        for row in cursor:
            album_id = row['album_id']
            playlist_id = row['playlist_id']
            if playlist_id not in result.keys():
                result[playlist_id] = []
                result[playlist_id].append(album_id)
            else:
                result[playlist_id].append(album_id)

        cursor.close()
        conn.close()
        return result