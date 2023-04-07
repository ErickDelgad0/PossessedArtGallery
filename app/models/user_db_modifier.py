from unittest import result
import mysql.connector

class User:
    """
    Initialize a users object using its username and password.

    :param username: username of the user
    :param password: password associated to the username
    """
    def __init__(self, username, password, first=None, last=None, email=None, description=None,  id=None):
        self._username = username
        self._password = password
        self._first = first
        self._last = last
        self._email = email
        self._description = description
        self._id = id
    
    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def first(self):
        return self._first
        
    @property
    def last(self):
        return self._last

    @property
    def email(self):
        return self._email

    @property
    def description(self):
        return self._description

    @property
    def id(self):
        return self._id

class UserDB:
    """
    This class provides an interface for interacting with a database of Users.
    """

    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor


    def get_username(self, user_name):
        query_username = 'SELECT * FROM Users WHERE username=%s;'
        
        self._cursor.execute(query_username, (user_name,))
        username_record = self._cursor.fetchone()

        return username_record
    
    def get_usernames_id(self, username):
        query_id = 'SELECT * FROM Users WHERE username=%s;'
        
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()

        return id_record

    def get_id(self, username, password):
        id_record = 0
        query_id = 'SELECT * FROM Users WHERE username=%s and password=%s;'
        
        self._cursor.execute(query_id, (username, password))
        id_record = self._cursor.fetchone()

        return id_record
    
    def get_password(self, pass_word):
        query_password = 'SELECT * FROM Users WHERE password=%s;'
        
        self._cursor.execute(query_password, (pass_word,))
        password_record = self._cursor.fetchone()

        return password_record


    def update_password(self, id, new_password):
        update_query = """
            UPDATE Users
            SET password=%s
            WHERE id=%s;
        """

        self._cursor.execute(update_query, (new_password, id))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()

        return user_id
    
    def update_first_name(self, id, new_first):
        update_query = """
            UPDATE Users
            SET first_name=%s
            WHERE id=%s;
        """

        self._cursor.execute(update_query, (new_first, id))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()
        return user_id

    def update_last_name(self, id, new_last):
        update_query = """
            UPDATE Users
            SET last_name=%s
            WHERE id=%s;
        """

        self._cursor.execute(update_query, (new_last, id))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()

        return user_id

    def update_email(self, id, new_email):
        update_query = """
            UPDATE Users
            SET email=%s
            WHERE id=%s;
        """

        self._cursor.execute(update_query, (new_email, id))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()

        return user_id


    def update_description(self, id, new_description):
        update_query = """
            UPDATE Users
            SET description=%s
            WHERE id=%s;
        """

        self._cursor.execute(update_query, (new_description, id))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()

        return user_id  
    

    def add_user(self, accounts):
        """
        Add a new users username record to the database

        :param username: new username to be added to the database
        """

        insert_user_query = '''
            INSERT INTO Users (username, password)
            VALUES (%s, %s);
        '''

        self._cursor.execute(insert_user_query, (accounts._username, accounts._password))
        self._conn.commit()

        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        return new_user_id


    def delete_user(self, id):
        """
        Remove a user record from the database
        
        :param name: username of the user to be removed from the database
        """
        query = 'DELETE FROM Users WHERE id=%s;'
        query1 = 'DELETE FROM artwork WHERE id=%s'
        query2 = 'DELETE FROM CollectionExhibit WHERE id=%s'
        query3 = '''SELECT users.id as user_id, artwork.id as artwork_id, 
                    collectionexhibit.id as collection_id FROM users 
                    inner join artwork on users.id = artwork.pk_users inner join 
                    collectionexhibit on collectionexhibit.pk_artwork = artwork.id WHERE users.id = %s;'''
        

        self._cursor.execute(query3, (id,))
        result_set = self._cursor.fetchall()
        for result in result_set:
            self._cursor.execute(query2, (result['collection_id'],))
            self._cursor.execute(query1, (result['artwork_id'],))
        self._cursor.execute(query, (id,))
        self._conn.commit()
        
        print(self._cursor.rowcount, "record(s) affected")
        # self._cursor.close()


    def get_user_by_username(self, name):
        """
        Find a user's record in the database using the username

        :param name: username of the user
        :return: a username
        """

        query = '''
        SELECT a.username, a.password, a.id
        FROM Users a
        INNER JOIN password p
        ON a.user_id = p.id
        WHERE a.name = %s
        '''

        self._cursor.execute(query, (name,))

        accounts = []

        for row in self._cursor.fetchall():
            user = User(row[0], row[1], row[2], row[3])
            accounts.append(user)

        self._cursor.close()
        return accounts
    

    def user_check(self, user_name):
        person = self.get_username(user_name)
        if not person:
            return False
        else:
            return True
        
    def validate_user(self, user_name, given_password):
        persons_id = self.get_id(user_name, given_password)

        if persons_id:
            return True
        else:
            return False

    def disconnect(self):
        self._conn.close()
