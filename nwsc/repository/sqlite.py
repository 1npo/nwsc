import os
import sqlite3
import glob
from pathlib import Path
from loguru import logger
from nwsc.repository.base import BaseRepository


SQLITE_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schemas/sqlite/')


class SQLiteRepository(BaseRepository):
    """
    :param sqlite_path: The path to the SQLite database to open (default: in-memory)
    :param sqlite_schema: The path to a file containing the schema to initialize a new database with
    """

    def __init__(
        self,
        sqlite_path: str = ':memory:',
        sqlite_schema_path: str = SQLITE_SCHEMA_PATH
    ):
        self.sqlite_path = sqlite_path
        self.sqlite_schema_path = sqlite_schema_path
        self.conn = sqlite3.connect(self.sqlite_path)
        self.curs = self.conn.cursor()

        if self.sqlite_path == ':memory:':
            self._init_new_sqlite_db()
        else:
            # The database will be empty (no tables) if it was just created. If the db at sqlite_path is empty,
            # initialize a new database using the given sqlite_schema.
            if not self.curs.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall():
                self._init_new_sqlite_db()

    def _init_new_sqlite_db(self):
        schema_files = glob.glob(os.path.join(self.sqlite_schema_path, '*.sql'))
        for schema_file in schema_files:
            with open(schema_file) as file:
                self.curs.executescript(file.read())
                logger.debug(f'Created "{Path(schema_file).stem}" tables')
        logger.info(f'Initialized new SQLite3 database at {self.sqlite_path}')
    
    def get_all(self, table: str) -> list:
        res = self.curs.execute(f'SELECT * FROM {table}').fetchall()
        res_cols = [desc[0] for desc in self.curs.description]
        res_records = [{k:v for k,v in zip(res_cols, record)} for record in res]
        return res_records

    def get(
        self,
        table: str,
        id: int,
        id_field: str = 'id'
    ) -> list:
        res = self.curs.execute(f'SELECT * FROM {table} WHERE {id_field} = ?', str(id)).fetchall()
        res_cols = [desc[0] for desc in self.curs.description]
        res_records = [{k:v for k,v in zip(res_cols, record)} for record in res]
        return res_records
    
    def filter_by(self, table: str, filter: dict) -> list:
        if len(filter) == 1:
            key = list(filter.keys())[0]
            filter_str = f'WHERE IFNULL({key}, "") = :{key}'
        else:
            filter_str = ''
            for key in filter.keys():
                if not filter_str:
                    filter_str = f'WHERE IFNULL({key}, "") = :{key}'
                else:
                    filter_str += f' AND IFNULL({key}, "") = :{key}'
        
        res = self.curs.execute(f'SELECT * FROM {table} {filter_str}', filter).fetchall()
        res_cols = [desc[0] for desc in self.curs.description]
        res_records = [{k:v for k,v in zip(res_cols, record)} for record in res]
        return res_records
    
    def create(self, table: str, record: dict) -> int:
        if 'id' not in record:
            raise KeyError('`record` requires an "id" field, but none was provided')
        
        fields = ', '.join([k for k in record.keys()])
        named_params = ', '.join([f':{k}' for k in record.keys()])
        self.curs.execute(f'INSERT OR IGNORE INTO {table} ({fields}) VALUES ({named_params})', record)
        self.conn.commit()
        return self.curs.lastrowid

    def update(self, table: str, record: dict):
        if 'id' not in record:
            raise KeyError('`record` requires an "id" field, but none was provided')

        update_str = ', '.join([f'{k} = :{k}' for k in record.keys() if k != 'id'])
        self.curs.execute(f'UPDATE OR IGNORE {table} SET {update_str} WHERE id = :id', record)
        self.conn.commit()

    def delete(self, table: str, id: int):
        self.curs.execute(f'DELETE FROM {table} WHERE id = ?', str(id))
        self.conn.commit()

    def serialize(self, item):
        pass

    def deserialize(self, data):
        pass
