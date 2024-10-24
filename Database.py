import sqlite3

DATABASE_PATH = "db.sqlite3"

class Database():
    def _connect(self):
        connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        connection.execute("PRAGMA busy_timeout = 5000")  # Wait up to 5 seconds
        return connection

    def get(self, query:str) -> any:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
        finally:
            connection.close()
        return result
    
    def get_with_params(self, query:str, query_params: tuple) -> any:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, query_params)
            result = cursor.fetchone()
        finally:
            connection.close()
        return result

    def get_multiple(self, query:str) -> any:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        finally:
            connection.close()
        return result
    
    def execute(self, query:str) -> bool:
        connection = self._connect()
        try:
            connection.execute(query)
        except Exception:
            return False
        finally:
            connection.close()
        return True

    def execute_with_params(self, query:str, query_params:tuple) -> bool:
        connection = self._connect()
        try:
            connection.execute(query, query_params)
        except Exception:
            return False
        finally:
            connection.close()
        return True
    
    def execute_many(self, query:str, query_params:list) -> bool:
        connection = self._connect()
        try:
            connection.executemany(query, query_params)
        except Exception:
            return False
        finally:
            connection.close()
        return True

    def close(self):
        """Close the database connection."""
        self.connection.close()

db = Database()