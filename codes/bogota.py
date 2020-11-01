import os
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

from my_utils import (connect_db, exists_table, update_databasebog, make_query)

def estado(table_name, conn):
    casos = make_query(
        f"SELECT ESTADO, count(*) as cantidad FROM {table_name} WHERE ESTADO not null GROUP BY ESTADO ORDER BY cantidad",
        conn
    )

    _ , ax = plt.subplots()
    ax.pie(casos['cantidad'], startangle=-90, autopct='%1.1f%%')
    ax.legend(casos['ESTADO'], loc="upper center", ncol=2)
    ax.set_title("Estado contagiados")
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    plt.savefig('plots/estado')
    #plt.show()

def ubicacion(table_name, conn):
    casos = make_query(
        f"SELECT UBICACION, count(*) as cantidad FROM {table_name} WHERE UBICACION not null GROUP BY UBICACION ORDER BY cantidad",
        conn
    )

    _ , ax = plt.subplots()
    ax.pie(casos['cantidad'], wedgeprops=dict(width=0.5), startangle=-40, autopct='%1.1f%%')
    ax.legend(casos['UBICACION'], loc="upper center", ncol=2)
    ax.set_title("Ubicacion contagiados")
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    plt.savefig('plots/ubicacion')
    #plt.show()

def sexo_edad(table_name, conn):
    rango_edad = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-...']
    casosf = make_query(
        f"""SELECT SUM(CASE WHEN EDAD <= 9.0 THEN 1 ELSE 0 END) AS [0-9],
        SUM(CASE WHEN EDAD BETWEEN 10.0 AND 19.0 THEN 1 ELSE 0 END) AS [10-19],
        SUM(CASE WHEN EDAD BETWEEN 20.0 AND 29.0 THEN 1 ELSE 0 END) AS [20-29],
        SUM(CASE WHEN EDAD BETWEEN 30.0 AND 39.0 THEN 1 ELSE 0 END) AS [30-39],
        SUM(CASE WHEN EDAD BETWEEN 40.0 AND 49.0 THEN 1 ELSE 0 END) AS [40-49],
        SUM(CASE WHEN EDAD BETWEEN 50.0 AND 59.0 THEN 1 ELSE 0 END) AS [50-59],
        SUM(CASE WHEN EDAD BETWEEN 60.0 AND 69.0 THEN 1 ELSE 0 END) AS [60-69],
        SUM(CASE WHEN EDAD BETWEEN 70.0 AND 79.0 THEN 1 ELSE 0 END) AS [70-79],
        SUM(CASE WHEN EDAD >= 80 THEN 1 ELSE 0 END) AS [80-...]
        FROM {table_name}
        WHERE SEXO = 'F'""",
        conn
    )
    casosm = make_query(
        f"""SELECT SUM(CASE WHEN EDAD <= 9.0 THEN 1 ELSE 0 END) AS [0-9],
        SUM(CASE WHEN EDAD BETWEEN 10.0 AND 19.0 THEN 1 ELSE 0 END) AS [10-19],
        SUM(CASE WHEN EDAD BETWEEN 20.0 AND 29.0 THEN 1 ELSE 0 END) AS [20-29],
        SUM(CASE WHEN EDAD BETWEEN 30.0 AND 39.0 THEN 1 ELSE 0 END) AS [30-39],
        SUM(CASE WHEN EDAD BETWEEN 40.0 AND 49.0 THEN 1 ELSE 0 END) AS [40-49],
        SUM(CASE WHEN EDAD BETWEEN 50.0 AND 59.0 THEN 1 ELSE 0 END) AS [50-59],
        SUM(CASE WHEN EDAD BETWEEN 60.0 AND 69.0 THEN 1 ELSE 0 END) AS [60-69],
        SUM(CASE WHEN EDAD BETWEEN 70.0 AND 79.0 THEN 1 ELSE 0 END) AS [70-79],
        SUM(CASE WHEN EDAD >= 80 THEN 1 ELSE 0 END) AS [80-...]
        FROM {table_name}
        WHERE SEXO = 'M'""",
        conn
    )
    f = casosf.values.tolist()
    m = casosm.values.tolist()

    x = np.arange(len(rango_edad))
    width = 0.35
    fig, ax = plt.subplots()
    mujeres = ax.bar(x - width/2, f[0], width, label='Mujeres')
    hombres = ax.bar(x + width/2, m[0], width, label='Hombres')

    ax.set_ylabel('Contagios')
    ax.set_title('Contagios por sexo y edad')
    ax.set_xticks(x)
    ax.set_xticklabels(rango_edad)
    ax.legend()

    fig.tight_layout()
    fig.savefig('plots/sexo_edad.png')
    #plt.show()


def localidad(table_name, conn):
    casos = make_query(
        f"SELECT LOCALIDAD_ASIS, count(*) as cantidad FROM {table_name} WHERE LOCALIDAD_ASIS not null GROUP BY LOCALIDAD_ASIS ORDER BY cantidad",
        conn
    )
    casos.plot(x='LOCALIDAD_ASIS', y='cantidad', kind='barh', xlabel='Localidad', ylabel='contagios')
    plt.title('Contagio por localidad')
    plt.tight_layout()
    plt.savefig('plots/localidades.png')
    #plt.show()


def evolucion_casos(table_name, conn):
    casos = make_query(
        f"SELECT FECHA_DIAGNOSTICO, count(*) as cantidad FROM {table_name} WHERE FECHA_DIAGNOSTICO not null GROUP BY FECHA_DIAGNOSTICO ORDER BY FECHA_DIAGNOSTICO",
        conn
    )
    casos['FECHA_DIAGNOSTICO'] = pd.to_datetime(casos['FECHA_DIAGNOSTICO'])
    casos['FECHA_DIAGNOSTICO'] = casos['FECHA_DIAGNOSTICO'].dt.strftime("%m-%d")

    casos.plot(x='FECHA_DIAGNOSTICO', y='cantidad', xlabel='Dias', ylabel='contagios')
    plt.title('Evolucion de contagios en Bogota')
    plt.legend(['Contagios diagnosticados por dia'])
    plt.tight_layout()
    plt.savefig('plots/evolucion.png')
    #plt.show()


def plots(table_name, conn):
    print('\nGenerando las graficas, por favor espere ...')
    evolucion_casos(table_name, conn)
    localidad(table_name, conn)
    sexo_edad(table_name, conn)
    ubicacion(table_name, conn)
    estado(table_name, conn)

def main(csv_url, database_name, table_name):
    plt.close('all')
    conn = connect_db(database_name)
    if exists_table(conn, table_name):
        print('\nLos datos ya estan en la base de datos')
        y = input('Desea actualizar la base de datos? ([y]/[n]): ').lower()
        if y == 'y':
            print('Descargando los datos de Covid-19, por favor espere ...')
            update_databasebog(csv_url, table_name, conn)
    else:
        print('Descargando los datos de Covid-19, por favor espere ...')
        update_databasebog(csv_url, table_name, conn)
    
    plots(table_name, conn)



if __name__ == '__main__':
    direc_a = os.getcwd()
    print(direc_a)
    #csv_url = "datasets/osb_enftransm-covid-19_31_10_2020 (1).csv"
    csv_url = "https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19_31_10_2020.csv"
    if 'codes' in direc_a:
        database_name = "datasets/covid.db"
    else:
        database_name = "codes/datasets/covid.db"
    table_name = "covidbogota"

    main(csv_url, database_name, table_name)



