import mysql.connector
from models.user_db_modifier import UserDB, User
from models.artwork_db_modifier import artworkDB, ArtWork

class ArtCollection:
    """
    Initialize a ArtWork object using its collection name and description.

    :param exhibit_name: collection name
    :param description: description of collection
    """
    def __init__(self, exhibit_name, description, id=None):
        self._exhibit_name = exhibit_name
        self._description = description
        self._id = id

@property
def exhibit_name(self):
    return self._exhibit_name

@property
def description(self):
    return self._description

@property
def id(self):
    return self._id

class ArtCollectionDB:
    """
    This class provides an interface for interacting with a 
    database of ArtCollection.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor


    def add_art_collection(self, art_id, new_art_collection):
        """
        Add a new artwork record to the database artwork

        :param artwork_to_add: artwork object to be added to the database
        """

        insert_user_query = '''
            INSERT INTO CollectionExhibit (pk_artwork, exhibit_name, description)
            VALUES (%s, %s, %s);
        '''

        self._cursor.execute(insert_user_query, (art_id ,new_art_collection._exhibit_name, new_art_collection._description))
        self._conn.commit()

        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        # self._cursor.close()
        return new_user_id


    def get_collection(self, collection):
        """
            This function allows us to retrieve a given
            collection name for a specific artwork collection

            :param collection: name of the collection
        """
        query_collection_name = 'SELECT * FROM CollectionExhibit WHERE exhibit_name=%s;'
        
        self._cursor.execute(query_collection_name, (collection,))
        image_record = self._cursor.fetchone()

        # self._cursor.close()
        return image_record


    def get_description(self, description):
        """
            This function allows us to retrieve a given
            description for a specific artwork collection

            :param description: full description to look for
        """
        query_description = 'SELECT * FROM CollectionExhibit WHERE description=%s;'
        
        self._cursor.execute(query_description, (description,))
        description_record = self._cursor.fetchone()

        # self._cursor.close()
        return description_record


    def update_description(self, new_description):
        """
            This function allows us to update a given
            description for a specific artwork collection

            :param new_description: any new str description to add 
        """
        query_update_description = '''
            INSERT INTO artwork (description) VALUES (%s);
        '''

        self._cursor.execute(query_update_description, (new_description,))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        # self._cursor.close()

        return new_user_id


    def add_description(self, new_description):
        """
        Add a new description record to the artwork database

        :param new_description: new description to be added to artwork
        """

        insert_new_description_query = '''
            INSERT INTO artwork (description)
            VALUES (%s);
        '''

        self._cursor.execute(insert_new_description_query, (new_description._description,))
        self._conn.commit()

        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        # self._cursor.close()

        return new_user_id


    def delete_artwork(self, id):
        """
        Remove a artwork record from the database
        
        :param id: id of the artwork to be removed from the database
        """
        query = 'DELETE FROM CollectionExhibit WHERE id=%s;'


        self._cursor.execute(query, (id,))
        self._conn.commit()
        
        print(self._cursor.rowcount, "record(s) affected")
        # self._cursor.close()

    def disconnect(self):
        self._conn.close()
