import pytest

from modules.db import ini_db, concatenate_row_values

'''function to test
- connect db
- concat rows
- process table
- load stop words
- ini api
- load_vect
- load_corpus
- search '''

def test_database_connection(database_connection):
    assert database_connection.is_connected()