import os

import psycopg2
from util.consoleColors import colors
from boto.s3.connection import S3Connection


def open_connection(initDatabase=False):
    conn = None
    try:
        # connect to the PostgreSQL server
        print(colors.BOLD + colors.OKGREEN + 'Connecting to the PostgreSQL database...' + colors.ENDC)
        conn = psycopg2.connect(host=os.environ['DATABASE_HOST'],
                                database=os.environ['DATABASE_NAME'],
                                user=os.environ['DATABASE_USER'],
                                password=os.environ['DATABASE_PASS'])
        if initDatabase:
            init_database(connection=conn, dropCreate=True)

    except (Exception, psycopg2.DatabaseError) as error:
        print(colors.BOLD + colors.FAIL + error + colors.ENDC)

    return conn


def init_database(connection, dropCreate):
    cur = connection.cursor()
    print(colors.BOLD + colors.OKGREEN + 'Initialising database...' + colors.ENDC)

    if dropCreate:
        print('Dropping table "factchecks" if exists.')
        cur.execute('DROP TABLE IF EXISTS factchecks')

    print('Creating table "factchecks" if not exists.')
    cur.execute('CREATE TABLE IF NOT EXISTS factchecks (' +
                'id SERIAL PRIMARY KEY,' +
                'title VARCHAR(200),' +
                'description VARCHAR(1000),' +
                'url VARCHAR(300),' +
                'language VARCHAR(2),'
                'date DATE,' +
                'publisher VARCHAR(20),' +
                'thumbnail VARCHAR(200)'
                ');')

    connection.commit()

    # close the communication with the PostgreSQL
    cur.close()
