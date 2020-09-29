import pandas as pd
import sqlite3 as db
from utils.my_utils import *


def update_database(csv_url, conn):
    data = download_data(csv_url)
    data = rename_columns(data)
    save_data(data, table_name, conn)


def exists_table(conn, table_name):
    tables = make_query(
        f"SELECT name FROM sqlite_master WHERE type='table'", conn)
    return tables['name'].str.contains(table_name).any()


def main(csv_url, database_name, table_name):
    conn = connect_db(database_name)

    if exists_table(conn, table_name):
        print('Los datos ya estan en la base de datos')
        y = input('Desea actualizar la base de datos? ([y]/[n]): ').lower()
        if y == 'y':
            update_database(csv_url, conn)
    else:
        print('Descargando los datos de Covid-19')
        update_database(csv_url, conn)

    alldata = make_query(f"SELECT * FROM {table_name}", conn)
    print(alldata.shape)
    print(alldata.head())
    print(list(alldata.columns))
    close_db(conn)


if __name__ == '__main__':
    csv_url = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
    database_name = "datasets/covid.db"
    table_name = "covidt"

    main(csv_url, database_name, table_name)
