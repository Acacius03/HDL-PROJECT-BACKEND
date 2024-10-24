import sqlite3

class Database():
    def __init__(self, db_path:str) -> None:
        self.db_path = db_path

    def _connect(self):
        connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return connection

    def get(self, query:str) -> any:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    def get_with_params(self, query:str, query_params: tuple) -> any:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(query, query_params)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

    def get_multiple(self, query:str) -> any:
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    
    def execute(self, query:str) -> None:
        connection = self._connect()
        with connection:
            connection.execute(query)
        connection.close()

    def execute_with_params(self, query:str, query_params:tuple) -> None:
        connection = self._connect()
        with connection:
            connection.execute(query, query_params)
        connection.close()
    
    def execute_many(self, query:str, query_params:list) -> None:
        connection = self._connect()
        with connection:
            connection.executemany(query, query_params)
        connection.close()

    def close(self):
        self.connection.close()