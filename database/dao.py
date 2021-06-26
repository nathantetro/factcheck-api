import psycopg2
from util.consoleColors import colors


def open_connection(initDatabase=False):
    conn = None
    try:
        # connect to the PostgreSQL server
        print(colors.BOLD + colors.OKGREEN + 'Connecting to the PostgreSQL database...' + colors.ENDC)
        conn = psycopg2.connect(host="ec2-54-220-170-192.eu-west-1.compute.amazonaws.com",
                                database="d750vbn9efqubn",
                                user="wzzotxienhwpvw",
                                password="6b32fbd24590a371c2abc09674c1d060cd2077d00c56c77011d5fab6f456a2aa")
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
                'publisher VARCHAR(20)' +
                ');')

    connection.commit()

    # close the communication with the PostgreSQL
    cur.close()
