"""
Collection of functions to help establish the database
"""
import mysql.connector


# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE Users
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            username VARCHAR(16),
            password VARCHAR(12),
            first_name VARCHAR(15),
            last_name VARCHAR(15),
            email VARCHAR(320),
            description VARCHAR(150),
            CONSTRAINT pk_users PRIMARY KEY (id),
            CONSTRAINT unique_user_name UNIQUE (username)
        );
        """
    )

    cursor.execute(
        f""" 
        CREATE TABLE artwork
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            pk_users INT UNSIGNED NOT NULL,
            img_url VARCHAR(100),
            description VARCHAR(140),
            timestamp VARCHAR(35),
            style VARCHAR(25),
            exhibit_name VARCHAR(25),
            CONSTRAINT pk_artwork PRIMARY KEY (id),
            CONSTRAINT fk_users FOREIGN KEY (pk_users) REFERENCES Users(id)
        );
        """
    )

    cursor.execute(
        f""" 
        CREATE TABLE CollectionExhibit
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            pk_artwork INT UNSIGNED NOT NULL,
            exhibit_name VARCHAR(25),
            description VARCHAR(140),
            CONSTRAINT pk_collection PRIMARY KEY (id),
            CONSTRAINT fk_artwork FOREIGN KEY (pk_artwork) REFERENCES artwork(id),
            CONSTRAINT unique_exhibit_name UNIQUE (exhibit_name)
        );
        """
    )

    cursor.close()
    conn.close()
