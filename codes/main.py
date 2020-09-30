import os
import pandas as pd
import sqlite3 as db
from my_utils import *
import matplotlib.pyplot as plt


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
    # torta_por_genero(conn,table_name)
    # muertos_por_Depto(conn,table_name)
    # activos_por_Depto(conn,table_name)
    # recuperados_por_Depto(conn,table_name)
    # contagiiados_por_edad(conn,table_name)
    torta_por_Tipo_Contagio(conn,table_name)

def torta_por_genero(conn,table_name):
    data = make_query(
        f"SELECT sexo, count(sexo) as cantidad FROM {table_name} WHERE sexo = 'F'  OR sexo = 'M' GROUP BY sexo", conn)
    y=data['cantidad']
    plt.figure()
    plt.title('Procentaje de contagiados por sexo')
    plt.pie(y,
            labels=['Femenino','masculino'],
            autopct='%1.1f%%',
            shadow=True)    
    plt.show()

def muertos_por_Depto(conn,table_name):
    data = make_query(
     f"select departamento ,count(*) as total from {table_name} WHERE atencion='Fallecido' GROUP BY departamento", conn)
    dept=data['departamento']
    cont=data['total']
    plt.figure()
    plt.title('Fallecimientos por departamento')
    plt.barh(dept,cont)  
    plt.show()
    

def activos_por_Depto(conn,table_name):
    data = make_query(
     f"select departamento , count(*) as total from {table_name}  GROUP BY departamento", conn)
    dept=data['departamento']
    cont=data['total']
    plt.figure()
    plt.title('Infectados por departamento')
    plt.barh(dept,cont)  
    plt.show()
    
def recuperados_por_Depto(conn,table_name):
    data = make_query(
     f"select departamento ,count(*) as total from {table_name} WHERE atencion='Recuperado' GROUP BY departamento", conn)
    dept=data['departamento']
    cont=data['total']
    plt.figure()
    plt.title('Recuperados por departamento')
    plt.barh(dept,cont)  
    plt.show()

def contagiiados_por_edad(conn,table_name):
    # Dispersion
     data = make_query(
        f"SELECT edad ,count(*) as total  FROM {table_name}  GROUP BY Edad", conn)
     fig, ax=plt.subplots()
     plt.title('Dispersión por edad de infectados')
     plt.xlabel('Edad(años)')
     plt.ylabel('Infectados')
     ax.scatter(data['edad'],data['total'])
     plt.show()

def torta_por_Tipo_Contagio(conn,table_name):
    data = make_query(
        f"SELECT atencion,count(*) as cantidad FROM {table_name} where atencion !='Recuperado' and atencion !='Fallecido' GROUP BY atencion", conn)
    print(data)
    y=data['cantidad']
    plt.figure()
    plt.title('Procentaje de contagiados por sexo')
    plt.pie(y,
            labels=['','En casa','Hospital', 'UCI'],
            autopct='%1.1f%%',
            shadow=True)    
    plt.show()

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
    direc_a = os.getcwd()
    print(direc_a)
    csv_url = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
    if 'codes' in direc_a:
        database_name = "datasets/covid.db"
    else:
        database_name = "codes/datasets/covid.db"
    table_name = "covidt"

    main(csv_url, database_name, table_name)
