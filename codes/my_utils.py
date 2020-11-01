import pandas as pd
import sqlite3 as db
from sqlite3 import Error


def download_data(url):
    """
    Descarga los datos en formato csv
    """
    return pd.read_csv(url, low_memory=False,parse_dates=['Fecha de notificación', 'Fecha de muerte', 'Fecha de recuperación', 'Fecha de diagnóstico', 'fecha reporte web'], dayfirst=True)


def download_databog(url):
    """
    Descarga los datos en formato csv
    """
    return pd.read_csv(url, sep=";", engine='python', encoding = "ISO-8859-1", dayfirst=True, parse_dates=['FECHA_DIAGNOSTICO', 'FECHA_INICIO_SINTOMAS'])


def connect_db(database_name):
    """
    Crea una conexion con la base de datos
    In: database_name - nombre de la base de datos
    Out: conn - conexion, objeto que representa la base de datos.
    """
    conn = None
    try:
        conn = db.connect(database_name)
        print(f'database connected {db.version}')
        return conn
    except Error as e:
        print(e)
        exit(1)

def exists_table(conn, table_name):
    tables = make_query(
        f"SELECT name FROM sqlite_master WHERE type='table'", conn)
    return tables['name'].str.contains(table_name).any()

def update_database(csv_url, table_name, conn):
    data = download_data(csv_url)
    print('Datos descargados ...')
    data = rename_columns1(data)
    save_data(data, table_name, conn)
    print('Datos almcenados en la base de datos ...')

def update_databasebog(csv_url,table_name, conn):
    data = download_databog(csv_url)
    print('Datos descargados ...')
    save_data(data, table_name, conn)
    print('Datos almcenados en la base de datos ...')

def close_db(conn):
    """
    Cierra la conexion con la base de datos
    In: conexion de la base de datos
    """
    conn.commit()
    conn.close()


def save_data(data, table_name, conn):
    """
    Guarda los datos descargados en la base de datos
    """
    data.to_sql(table_name, conn, if_exists='replace', index=False)


def make_query(query_statement, conn):
    return pd.read_sql(query_statement, conn)


def rename_columns1(data):
    return data.rename(columns={
        'ID de caso': 'id',
        'Fecha de notificación': 'f_notificacion',
        'Código DIVIPOLA departamento': 'DIVIPOLAdep',
        'Código DIVIPOLA municipio' : 'DIVIPOLAmun',
        'Ciudad de ubicación': 'ciudad',
        'Nombre departamento': 'departamento',
        'Nombre municipio' : 'municipio',
        'Ubicación del caso': 'ubicacion_caso',
        'Recuperado': 'atencion',
        'Edad': 'edad',
        'Sexo': 'sexo',
        'Estado': 'estado',
        'País de procedencia': 'procedencia',
        'FIS': 'FIS',
        'Fecha de muerte': 'f_muerte',
        'Fecha de diagnóstico': 'f_diagnostico',
        'Fecha de recuperación': 'f_recuperado',
        'fecha reporte web': 'f_reporteweb',
        'Tipo de recuperación': 'tipo_recuperacion',
        'Tipo de contagio' : 'tipo_contagio',
        'Codigo departamento': 'cod_departamento',
        'Codigo pais': 'cod_pais',
        'Pertenencia étnica': 'etnia',
        'Nombre del grupo étnico': 'nombre_etnia'
    })
