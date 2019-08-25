import logging
import os

import psycopg2


class DbConnection(object):
    """Connect to Postgres Sql"""

    def __init__(self,
                 dbname='postgres',
                 user='postgres',
                 password='pNHh5LHa2k',
                 host='postgres-postgresql',
                 port='5432'):

        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    connect_timeout=3)
            cur = self.connection.cursor()
            cur.execute('SELECT version()')
            db_version = cur.fetchone()
            logging.info(
                    'Successfully connected to Postgres %s to database %s',
                    db_version, dbname)
        except Exception as e:
            logging.error('Failed to connect !' + str(e))
            raise e

    def __del__(self):
        self.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute_query(self, query):
        """execute_query."""
        try:
            rows = None
            cursor = self.connection.cursor()
            cursor.execute(query)
            if cursor.rowcount > 0 and cursor.description:
                rows = cursor.fetchall()
            cursor.close()
            return rows

        except (Exception, psycopg2.DatabaseError) as error:
            logging.warn('Failed to execute ' + query + str(error))
            raise error

    def execute_sql(self, script):
        """Execute sql commands from a file."""
        if os.path.exists(script):
            data = open(script).read()
            self.execute_query(data)
            self.commit()
        else:
            logging.warn('initDb: %s not found', script)
            raise
