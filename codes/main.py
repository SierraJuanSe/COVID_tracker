import os
from os import terminal_size
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

from my_utils import *


def plot_data(conn, table_name):
    print('Generando las graficas, por favor espere ...')
    diarios(conn, table_name)
    torta_por_genero(conn, table_name)
    muertos_por_Depto(conn, table_name)
    activos_por_Depto(conn, table_name)
    recuperados_por_Depto(conn, table_name)
    contagiiados_por_edad(conn, table_name)
    torta_por_Tipo_Contagio(conn, table_name)


def diarios(conn, table_name):
    datainf = make_query(
        f"SELECT f_notificacion as mes_not, count(*) as cantidad FROM {table_name} GROUP BY mes_not ORDER BY mes_not", conn)
    datainf['mes_not'] = pd.to_datetime(datainf['mes_not'])
    datainf['mes_not'] = datainf['mes_not'].dt.strftime("%m-%d")
    datarec = make_query(
        f"SELECT f_recuperado as mes_not, count(*) as cantidad FROM {table_name} WHERE mes_not IS NOT NULL GROUP BY mes_not ORDER BY mes_not", conn)
    datarec['mes_not'] = pd.to_datetime(datarec['mes_not'])
    datarec['mes_not'] = datarec['mes_not'].dt.strftime("%m-%d")
    datamuer = make_query(
        f"SELECT f_muerte as mes_not, count(*) as cantidad FROM {table_name} WHERE mes_not IS NOT NULL GROUP BY mes_not ORDER BY mes_not", conn)
    datamuer['mes_not'] = pd.to_datetime(datamuer['mes_not'])
    datamuer['mes_not'] = datamuer['mes_not'].dt.strftime("%m-%d")
    xinf = datainf['mes_not']
    yinf = datainf['cantidad']
    xrec = datarec['mes_not']
    yrec = datarec['cantidad']
    xmuer = datamuer['mes_not']
    ymuer = datamuer['cantidad']

    fig, ax = plt.subplots()
    plt.title('Curva de contagiados en el tiempo(diario)')
    ax.plot(xinf, yinf)
    ax.plot(xrec, yrec)
    ax.plot(xmuer, ymuer)
    plt.legend(['Contagiados', 'Recuperados', 'Muertos'])
    plt.title(
        'Comparacion contagios, recuperados y muertos en el tiempo(diarios')
    # this locator puts ticks at regular intervals
    loc = ticker.MultipleLocator(base=12)
    ax.xaxis.set_major_locator(loc)
    plt.show()


def torta_por_genero(conn, table_name):
    data = make_query(
        f"SELECT sexo, count(sexo) as cantidad FROM {table_name} WHERE sexo = 'F'  OR sexo = 'M' GROUP BY sexo", conn)
    y = data['cantidad']
    plt.figure()
    plt.title('Procentaje de contagiados por sexo')
    plt.pie(y,
            labels=['Femenino', 'masculino'],
            autopct='%1.1f%%',
            shadow=True)
    plt.show()


def muertos_por_Depto(conn, table_name):
    data = make_query(
        f"select departamento ,count(*) as total from {table_name} WHERE atencion='Fallecido' GROUP BY departamento ORDER BY total", conn)
    dept = data['departamento']
    cont = data['total']
    plt.figure()
    plt.title('Diez Departamentos con mas Fallecimientos')
    plt.barh(dept[-10:], cont[-10:])
    plt.show()


def activos_por_Depto(conn, table_name):
    data = make_query(
        f"select departamento , count(*) as total from {table_name}  GROUP BY departamento ORDER BY total", conn)
    dept = data['departamento']
    cont = data['total']
    plt.figure()
    plt.title('Diez Departamentos con mas Contagiados')
    plt.barh(dept[-10:], cont[-10:])
    plt.show()


def recuperados_por_Depto(conn, table_name):
    data = make_query(
        f"select departamento ,count(*) as total from {table_name} WHERE atencion='Recuperado' GROUP BY departamento ORDER BY total", conn)
    dept = data['departamento']
    cont = data['total']
    plt.figure()
    plt.title('Diez Departamentos con mas recuperados')
    plt.barh(dept[-10:], cont[-10:])
    plt.show()


def contagiiados_por_edad(conn, table_name):
    # Dispersion
    data = make_query(
        f"SELECT edad ,count(*) as total  FROM {table_name}  GROUP BY Edad", conn)
    fig, ax = plt.subplots()
    plt.title('Dispersión por edad de infectados')
    plt.xlabel('Edad(años)')
    plt.ylabel('Infectados')
    ax.scatter(data['edad'], data['total'])
    plt.show()


def torta_por_Tipo_Contagio(conn, table_name):
    data = make_query(
        f"SELECT ubicacion_caso ,count(*) as cantidad FROM {table_name} where ubicacion_caso !='Recuperado' and ubicacion_caso !='Fallecido' GROUP BY ubicacion_caso", conn)
    y = data['cantidad']
    plt.figure()
    plt.title('Porcentaje de atención de contagiados')
    plt.pie(y,
            labels=['', 'En casa', 'Hospital', 'UCI'],
            autopct='%1.1f%%',
            shadow=True)
    plt.show()


def main(csv_url, database_name, table_name):
    plt.close('all')
    conn = connect_db(database_name)

    if exists_table(conn, table_name):
        print('Los datos ya estan en la base de datos')
        y = input('Desea actualizar la base de datos? ([y]/[n]): ').lower()
        if y == 'y':
            print('Descargando los datos de Covid-19, por favor espere ...')
            update_database(csv_url, table_name, conn)
    else:
        print('Descargando los datos de Covid-19, por favor espere ...')
        update_database(csv_url, table_name, conn)

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
