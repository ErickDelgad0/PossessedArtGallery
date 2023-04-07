import mysql.connector
from models.user_db_modifier import UserDB, User

class ArtWork:
    """
    Initialize a ArtWork object using its image URL and artwork decription.

    :param img_url: username of the user
    :param description: password associated to the username
    :param timestamp: when the artwork was uploaded
    :param artstyle: style of the work
    """
    def __init__(self, Users_id, img_url, description, timestamp, artstyle, collection_name, id=None):
        self._Users_id = Users_id
        self._img_url = img_url
        self._description = description
        self._timestamp = timestamp
        self._artstyle = artstyle
        self._collection_name = collection_name
        self._id = id

@property
def Users_id(self):
    return self._Users_id

@property
def img_url(self):
    return self._img_url

@property
def description(self):
    return self._description

@property
def timestamp(self):
    return self._timestamp

@property
def artstyle(self):
    return self._artstyle

@property
def collection_name(self):
    return self._collection_name

@property
def id(self):
    return self._id

class artworkDB:
    """
    This class provides an interface for interacting with a database of artwork.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor


    def add_artwork(self, new_artwork):
        """
        Add a new artwork record to the database artwork

        :param artwork_to_add: artwork object to be added to the database
        """

        insert_user_query = '''
            INSERT INTO artwork (pk_users, img_url, description, timestamp, style, exhibit_name)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

        self._cursor.execute(insert_user_query,(new_artwork._Users_id, new_artwork._img_url, new_artwork._description, new_artwork._timestamp, new_artwork._artstyle, new_artwork._collection_name))
        self._conn.commit()

        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()

        return new_user_id


    def get_image(self, img_url):
        """
            This function allows us to retrieve a given
            image url for a specific artwork
        """
        query_image_url = 'SELECT * FROM artwork WHERE img_url=%s;'
        
        self._cursor.execute(query_image_url, (img_url,))
        image_record = self._cursor.fetchone()

        # self._cursor.close()
        return image_record
    

    def get_artwork(self, artstyle, exhibit_name):
        """
            This function allows us to retrieve an artwork based
            on the matching artsyle and exhibit name
        """
        query_artwork = 'SELECT * FROM artwork WHERE style=%s and exhibit_name=%s;'

        self._cursor.execute(query_artwork, (artstyle, exhibit_name))
        artwork_found = self._cursor.fetchone()

        # self._cursor.close()
        return artwork_found


    def get_description(self, description):
        """
            This function allows us to retrieve a given
            description for a specific artwork
        """
        query_description = 'SELECT * FROM artwork WHERE description=%s;'
        
        self._cursor.execute(query_description, (description,))
        description_record = self._cursor.fetchone()

        # self._cursor.close()
        return description_record


    def get_artstyle(self, artstyle):
        """
            This function allows us to retrieve a given
            description for a specific artwork
        """
        query_artstyle = 'SELECT * FROM artwork WHERE style=%s;'
        
        self._cursor.execute(query_artstyle, (artstyle,))
        artstyle_record = self._cursor.fetchone()

        # self._cursor.close()
        return artstyle_record
    
    def get_collection_name(self, collection_name):
        """
            This function allows us to retrieve a given
            collection_name for a specific artwork
        """
        query_collection_name = 'SELECT * FROM artwork WHERE exhibit_name=%s;'
        
        self._cursor.execute(query_collection_name, (collection_name,))
        exhibit_name_record = self._cursor.fetchone()

        # self._cursor.close()
        return exhibit_name_record

    def get_collection(self, collection_name):
        """
            This function allows us to retrieve a given
            description for a specific artwork
        """
        collection_name = 'SELECT * FROM artwork WHERE style=%s;'
        
        self._cursor.execute(collection_name, (artstyle,))
        collection_name_record = self._cursor.fetchone()

        # self._cursor.close()
        return collection_name_record


    def update_description(self, new_description):
        """
            This function allows us to update a given
            description for a specific artwork
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
        query = 'DELETE FROM artwork WHERE id=%s;'


        self._cursor.execute(query, (id,))
        self._conn.commit()
        
        print(self._cursor.rowcount, "record(s) affected")
        # self._cursor.close()

    def disconnect(self):
        self._conn.close()
