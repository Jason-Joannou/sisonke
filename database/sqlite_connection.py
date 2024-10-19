import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQLiteConnection:

    def __init__(self, database=None):

        if database is not None:
            self.database = database
            self._engine = None
        else:
            raise ValueError(
                f"Database connection not established, connection = {database}"
            )

    def get_engine(self):

        if not os.path.exists(self.database):
            raise FileNotFoundError(f"SQLite database file '{self.database}' not found")

        if not self._engine:
            try:
                self._engine = create_engine(f"sqlite:///{self.database}")
            except Exception as e:
                logging.error("Error creating SQL engine: %s", e)
                raise
        return self._engine

    def get_session(self):

        session = sessionmaker(bind=self.get_engine())
        return session()

    def connect(self):

        try:
            connection = self.get_engine().connect()
            return connection
        except Exception as e:
            logging.error("Error establishing SQL connection: %s", e)
            raise

    def test_connection(self):

        try:
            connection = self.get_engine().connect()
            response = {
                "connection_status": "complete",
                "message": "Successfully established SQLite connection.",
            }
            connection.close()
            return response
        except ValueError as e:
            response = {
                "connection_status": "incomplete",
                "message": f"Error establishing SQLite connection: {e}",
            }
            return response
