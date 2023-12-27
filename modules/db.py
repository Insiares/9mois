from sqlalchemy import create_engine, MetaData, Table


def connect_db():
    url = "mysql+pymysql://root:root@9mois.ownedge.fr:3306/9mois"
    engine = create_engine(url)
    metadata = MetaData()
    return engine, metadata


def process_table(engine, metadata, table_name):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        result_set = connection.execute(table.select()).fetchall()
    return result_set
