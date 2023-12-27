from sqlalchemy import create_engine, MetaData, Table


def connect_db():
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/9mois")
    metadata = MetaData()
    return engine, metadata

# Fonction pour concaténer les valeurs textuelles de toutes les colonnes
def concatenate_row_values(row):
    return ''.join(str(value) for value in row if isinstance(value, str))


def process_table(engine, metadata,table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        result_set = connection.execute(table.select()).fetchall()
    concatenated_docs = [concatenate_row_values(row) for row in result_set]
    return concatenated_docs