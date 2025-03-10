import oracledb

class DBManager:
    def __init__(self, in_docker=False):
        """
        Initializes the database manager with the correct connection parameters.

        Args:
            dev_db (bool): Determines if the connection should be to the development database.
            in_docker (bool): Specifies if the application is running in a Docker container.
        """
        port = 6000

        # Choose DSN based on environment (local or Docker)
        if in_docker:
            # Use container hostname for Docker setup
            hostname = 'cabal-events-utils-database-1'
            port = 1521
        else:
            hostname = 'localhost'

        self.__username = 'sys'
        self.__password = 'admin'
        self.__dsn = f'{hostname}:{port}/xe'

    def __yield_connection(self):
        """
        Yields a connection to the Oracle database.
        
        Returns:
            oracledb.Connection: A connection to the Oracle database.
        """
        return oracledb.connect(user=self.__username, password=self.__password, dsn=self.__dsn, mode=oracledb.AUTH_MODE_SYSDBA)

    def run_query(self, query, query_details=None):
        """
        Executes a query and returns the results.

        Args:
            query (str): SQL query to execute.
            query_details (dict, optional): Parameters for the SQL query.

        Returns:
            list: The results of the query.
        """
        with self.__yield_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, query_details)
            return cursor.fetchall()

    def execute_insert(self, query, data_dict):
        """
        Executes an insert query and commits the changes.

        Args:
            query (str): SQL insert statement.
            data_dict (dict): Data to insert.

        Returns:
            None
        """
        with self.__yield_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data_dict)
            connection.commit()

    def execute_delete(self, query, data_dict=None):
        """
        Executes a DELETE query and commits the changes.
    
        Args:
            query (str): SQL delete statement.
            data_dict (dict, optional): Parameters for the SQL delete statement.
    
        Returns:
            int: The number of rows deleted.
        """
        with self.__yield_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data_dict)
            rows_deleted = cursor.rowcount
            connection.commit()
            return rows_deleted

    def execute_update(self, query, data_dict=None):
        """
        Executes an UPDATE query and commits the changes.

        Args:
            query (str): SQL update statement.
            data_dict (dict, optional): Parameters for the SQL update statement.

        Returns:
            int: The number of rows updated.
        """
        with self.__yield_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, data_dict)
            rows_updated = cursor.rowcount
            connection.commit()
            return rows_updated
