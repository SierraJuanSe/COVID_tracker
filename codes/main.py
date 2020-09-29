import pandas as pd
import sqlite3 as db
from my_utils import *


def update_database(csv_url, conn):
    data = download_data(csv_url)
    print('Datos descargados ...')
    data = rename_columns(data)
    save_data(data, table_name, conn)
    print('Datos almcenados en la base de datos ...')


def exists_table(conn, table_name):
    tables = make_query(
        f"SELECT name FROM sqlite_master WHERE type='table'", conn)
    return tables['name'].str.contains(table_name).any()


def plot_data(conn, table_name):
    print('Generando las graficas, por favor espere ...')

    alldata = make_query(
        f"SELECT sexo, count(sexo) FROM {table_name} WHERE sexo = 'F'  OR sexo = 'M' GROUP BY sexo", conn)
    print(alldata)


def main(csv_url, database_name, table_name):
    conn = connect_db(database_name)

    if exists_table(conn, table_name):
        print('Los datos ya estan en la base de datos')
        y = input('Desea actualizar la base de datos? ([y]/[n]): ').lower()
        if y == 'y':
            print('Descargando los datos de Covid-19, por favor espere ...')
            update_database(csv_url, conn)
    else:
        print('Descargando los datos de Covid-19, por favor espere ...')
        update_database(csv_url, conn)

    plot_data(conn, table_name)
    close_db(conn)


if __name__ == '__main__':
    csv_url = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
    database_name = "datasets/covid.db"
    table_name = "covidt"

    main(csv_url, database_name, table_name)
