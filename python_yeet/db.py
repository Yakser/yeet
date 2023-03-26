from pymysql import connect

from python_yeet.orm import BaseManager


class Database:
    _instance = None

    def __init__(self, db_settings: dict, init_queries=None):
        self.conn = connect(host=db_settings['host'],
                            user=db_settings['user'],
                            password=db_settings['password'],
                            database=db_settings['database'])
        self.cursor = self.conn.cursor()

        # IDK why pymysql cant create multiple tables in one query, so I have to use init_queries
        if init_queries:
            for query in init_queries:
                self.cursor.execute(query)
                self.conn.commit()
        self.cursor.close()
        self.conn.close()

        BaseManager.set_connection(db_settings=db_settings)
