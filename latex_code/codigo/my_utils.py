import pandas as pd
import sqlite3 as db
from sqlite3 import Error


def download_data(url):
    """
    Descarga los datos en formato csv
    """
    return pd.read_csv(url, low_memory=False)


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


def rename_columns(data):
    return data.rename(columns={
        'ID de caso': 'id',
        'Fecha de notificación': 'f_notificacion',
        'Código DIVIPOLA': 'DIVIPOLA',
        'Ciudad de ubicación': 'ciudad',
        'Departamento o Distrito ': 'departamento',
        'atención': 'atencion',
        'Edad': 'edad',
        'Sexo': 'sexo',
        'Estado': 'estado',
        'País de procedencia': 'procedencia',
        'FIS': 'FIS',
        'Fecha de muerte': 'f_muerte',
        'Fecha diagnostico': 'f_diagnostico',
        'Fecha recuperado': 'f_recuperado',
        'fecha reporte web': 'f_reporteweb',
        'Tipo recuperación': 'tipo_recuperacion',
        'Codigo departamento': 'cod_departamento',
        'Codigo pais': 'cod_pais',
        'Pertenencia etnica': 'etnia',
        'Nombre grupo etnico': 'nombre_etnia'
    })
