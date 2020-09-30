import os
from matplotlib.pyplot import subplot
from numpy.core.shape_base import block
import pandas as pd
import sqlite3 as db
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

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


def diarios(conn, table_name):
    datainf = make_query(
        f"SELECT strftime('%m-%d', f_notificacion) as mes_not, count(*) as cantidad FROM {table_name} GROUP BY mes_not", conn)
    datarec = make_query(
        f"SELECT strftime('%m-%d', f_recuperado) as mes_not, count(*) as cantidad FROM {table_name} GROUP BY mes_not", conn)

    datarec.set_index('mes_not')

    x = datainf['mes_not']
    inf = datainf['cantidad']
    xrec = datarec['mes_not']
    rec = datarec['cantidad']
    fig, ax = plt.subplots()
    ax.plot(x, inf)
    ax.legend(['Infectados por dia', 'Recuperados por dia'])
    loc = plticker.MultipleLocator(base=30.0)
    ax.xaxis.set_major_locator(loc)
    plt.title('numero de casos por dia')
    plt.show()


def plot_data(conn, table_name):
    print('Generando las graficas, por favor espere ...')
    diarios(conn, table_name)
    casos_id(conn, table_name)


def main(csv_url, database_name, table_name):
    plt.close('all')
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
    direc_a = os.getcwd()
    print(direc_a)
    csv_url = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
    if 'codes' in direc_a:
        database_name = "datasets/covid.db"
    else:
        database_name = "codes/datasets/covid.db"
    table_name = "covidt"

    main(csv_url, database_name, table_name)
