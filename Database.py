import sqlite3

DATABASE_PATH = "db.sqlite3"

class Database():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    def get(self, query:str) -> any:
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    
    def get_with_params(self, query:str, query_params: tuple) -> any:
        cursor = self.connection.cursor()
        cursor.execute(query, query_params)
        return cursor.fetchone()

    def get_multiple(self, query:str) -> any:
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def execute(self, query:str) -> bool:
        with self.connection as cmd:
            cmd.execute(query)
        return True

    def execute_with_params(self, query:str, query_params:tuple) -> bool:
        with self.connection as cmd:
            cmd.execute(query, query_params)
        return True
    
    def execute_many(self, query:str, query_params:list) -> bool:
        with self.connection as cmd:
            cmd.executemany(query, query_params)
        return True

    def close(self):
        """Close the database connection."""
        self.connection.close()

db = Database()