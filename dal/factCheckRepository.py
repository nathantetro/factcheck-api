import psycopg2
from database import dao
from domain.FactCheck import FactCheck
from util.consoleColors import colors


def create_factcheck_bulk(factChecks, initDatabase=False):
    print(
        colors.BOLD + colors.OKBLUE + "===================== STARTED BULK INSERT FACTCHECKS =====================" + colors.BOLD + colors.OKBLUE)
    dao.open_connection(initDatabase=initDatabase)
    for i in range(len(factChecks)):
        create_factcheck(factChecks[i])
    print(
        colors.BOLD + colors.OKBLUE + "===================== FINISHED BULK INSERT FACTCHECKS =====================" + colors.ENDC)


def create_factcheck(factCheck):
    connection = dao.open_connection()
    cur = connection.cursor()

    print(colors.OKGREEN + 'Inserting factcheck into database...' + colors.ENDC)
    cur.execute(
        'INSERT INTO factchecks(title,description,url,language,date,publisher)'
        ' VALUES(%s, %s, %s,%s,%s,%s);',
        (factCheck.title,
         factCheck.description,
         factCheck.url, factCheck.language, factCheck.date, factCheck.publisher))

    connection.commit()
    cur.close()


def read_all_factchecks():
    conn = None
    factchecks = []
    try:
        conn = dao.open_connection()
        cur = conn.cursor()
        cur.execute("SELECT title, description, url, language, date, publisher FROM factchecks")
        row = cur.fetchone()

        while row is not None:
            factchecks.append(FactCheck(row[0], row[1], row[4], row[2], row[5], row[3]).__dict__)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colors.BOLD + colors.FAIL + error + colors.ENDC)
    finally:
        if conn is not None:
            conn.close()
        return factchecks


def read_factchecks_of_publisher(publisher):
    conn = None
    factchecks = []
    try:
        conn = dao.open_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT title, description, url, language, date, publisher FROM factchecks WHERE publisher='" + publisher + "'")
        row = cur.fetchone()

        while row is not None:
            factchecks.append(FactCheck(row[0], row[1], row[2], row[3], row[4], row[5]).__dict__)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colors.BOLD + colors.FAIL + error + colors.ENDC)
    finally:
        if conn is not None:
            conn.close()
        return factchecks
