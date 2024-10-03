'''
Visualizacion de datos

Introducción
El objetivo de estos laboratorios es presentarle la visualización de datos con Python de la forma más concreta y coherente posible. Hablando de coherencia, 
debido a que no existe la mejor biblioteca de visualización de datos disponible para Python, tenemos que presentar diferentes bibliotecas y mostrar sus beneficios
cuando discutimos nuevos conceptos de visualización. Al hacerlo, esperamos que los estudiantes tengan conocimientos completos de bibliotecas y conceptos de visualización
para que puedan juzgar y decidir cuál es la mejor técnica y herramienta de visualización para un problema y una audiencia determinados.

Asegúrese de haber completado los requisitos previos para este curso, a saber, conceptos básicos de Python para la ciencia de datos y análisis de datos con Python.

Nota: La mayoría de los gráficos y visualizaciones se generarán utilizando datos almacenados en marcos de datos de pandas. Por lo tanto, en esta práctica de laboratorio 
ofrecemos un breve curso intensivo sobre pandas. Sin embargo, si está interesado en aprender más sobre la biblioteca de pandas, en nuestro curso se proporciona
una descripción detallada y una explicación de cómo usarla y cómo limpiar, eliminar y procesar datos almacenados en un marco de datos de pandas. Análisis de datos con Python.


Tabla de contenido
Explorando conjuntos de datos con pandas
1.1 El conjunto de datos: inmigración a Canadá de 1980 a 2013
1.2 Conceptos básicos de pandas
1.3 pandas intermedio: indexación y selección
2. Visualización de datos usando Matplotlib
2.1 Matplotlib: biblioteca de visualización estándar de Python
3. Gráficos lineales

Explorando conjuntos de datos con pandas 
pandas es un conjunto de herramientas de análisis de datos esencial para Python. Desde su sitio web:

pandas es un paquete de Python que proporciona estructuras de datos rápidas, flexibles y expresivas diseñadas para hacer que trabajar con datos "relacionales" o "etiquetados"
sea fácil e intuitivo. Su objetivo es ser el componente fundamental de alto nivel para realizar análisis de datos prácticos y del mundo real en Python.

El curso se basa en gran medida en pandas para la discusión, el análisis y la visualización de datos. Le recomendamos que dedique algo de tiempo a familiarizarse con la referencia
de la API de pandas: http://pandas.pydata.org/pandas-docs/stable/api.html.

El conjunto de datos: inmigración a Canadá de 1980 a 2013 
Fuente del conjunto de datos: Flujos migratorios internacionales hacia y desde países seleccionados - Revisión de 2015.

El conjunto de datos contiene datos anuales sobre los flujos de inmigrantes internacionales registrados por los países de destino. Los datos presentan tanto las entradas como las
salidas según el lugar de nacimiento, ciudadanía o lugar de residencia anterior/siguiente tanto para extranjeros como para nacionales. La versión actual presenta datos pertenecientes
a 45 países.

En esta práctica de laboratorio, nos centraremos en los datos de inmigración canadiense.

Conceptos básicos de pandas
Lo primero que haremos será instalar openpyxl (anteriormente xlrd), un módulo que pandas necesita para leer archivos de Excel.
Si no se utiliza un entorno Jupyter y trabajamos con visualstudio instalar el siguiente módulo en vez del piplite
import aiohttp
'''
# Llama a la función asíncrona

#Lo siguiente que haremos será importar dos módulos clave de análisis de datos: pandas y numpy.
import aiohttp
import asyncio

import pandas as pd
import numpy as np
import io

import matplotlib as mpl
import matplotlib.pyplot as plt

#Descarguemos e importemos nuestro conjunto de datos principal de inmigración canadiense utilizando el método `read_excel()` de *pandas*.
# Función asíncrona para descargar el archivo
async def fetch_url(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            return await resp.read()

#Llamamos las funciones asíncronas que vayamos a utilizar

async def main():
    URL =  'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Canada.xlsx'
    data = await fetch_url(URL)
    text = io.BytesIO(data)

    df_can = pd.read_excel(
        text,
        sheet_name='Canada by Citizenship',
        skiprows=range(20),
        skipfooter=2
    )
    print('¡Datos descargados y leídos en un marco de datos!')
    return df_can
    
# Ejecutar la función principal
df_can = asyncio.run(main())

#Vemos las primeras 5 
print(df_can.head())
#También podemos ver las 5 filas inferiores del conjunto de datos usando la función `tail()`.
print(df_can.tail())
'''
Al analizar un conjunto de datos, siempre es una buena idea comenzar obteniendo información básica sobre su marco de datos. Podemos hacer esto usando el método info().

Este método se puede utilizar para obtener un breve resumen del marco de datos.
'''
print(df_can.info(verbose=False))
'''
Para obtener la lista de encabezados de columna, podemos recurrir a la variable de instancia de columnas del marco de datos.
De manera similar, para obtener la lista de índices usamos las variables de instancia .index.
'''
print(df_can.columns)
print(df_can.index)
#Nota: El tipo predeterminado de índice y columnas de variables de instancia NO son una lista.
print(type(df_can.columns))
print(type(df_can.index))
#Para obtener el índice y las columnas como listas, podemos usar el método tolist().
print(df_can.columns.tolist())
print(df_can.index.tolist())
print(type(df_can.columns.tolist()))
print(type(df_can.index.tolist()))
#Para ver las dimensiones del marco de datos, usamos la variable de instancia "forma" del mismo.
print(df_can.shape)
'''
Nota: Los principales tipos almacenados en los objetos pandas son float, int, bool, datetime64[ns], datetime64[ns, tz], timedelta[ns], categoría y objeto (cadena). 
Además, estos tipos tienen tamaños de elementos, p. int64 e int32.

En pandas el eje = 0 representa filas (predeterminado) y el eje = 1 representa columnas.

Limpiemos el conjunto de datos para eliminar algunas columnas innecesarias. Podemos usar el método pandas drop() de la siguiente manera:
'''
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)
print(df_can.head(2))
#Cambiemos el nombre de las columnas para que tengan sentido. Podemos usar el método `rename()` pasando un diccionario de nombres antiguos y nuevos de la siguiente manera:
df_can.rename(columns={'OdName': 'Pais', 'AreaName': 'Continente', 'RegName': 'Region'}, inplace=True)
print(df_can.columns)
#También agregaremos una columna 'Total' que resume el total de inmigrantes por país durante todo el período 1980 - 2013, de la siguiente manera:

df_can['Total'] = df_can.sum(axis=1, numeric_only=True)
#Podemos verificar cuántos objetos nulos tenemos en el conjunto de datos de la siguiente manera:
print(df_can.isnull().sum())
#Finalmente, veamos un resumen rápido de cada columna en nuestro marco de datos usando el método `describe()`
print(df_can.describe())

'''
Pandas Intermedio: Indexación y Selección (rebanado)
Seleccionar columna
Hay dos formas de filtrar por nombre de columna:

Método 1: Rápido y fácil, pero solo funciona si el nombre de la columna NO tiene espacios ni caracteres especiales.

    df.column_name # devuelve series
Método 2: más robusto y puede filtrar en varias columnas.

    df['columna'] # devuelve series
    df[['columna 1', 'columna 2']] # devuelve marco de datos

Ejemplo: Intentemos filtrar por la lista de países ('País').
'''
print(df_can.Pais)

#Intentemos filtrar por la lista de países ("País") y los datos por años: 1985 - 1989.
print(df_can[['Pais', 1985, 1986, 1987, 1988, 1989]])
# observe que 'País' es una cadena y los años son números enteros. 
# En aras de la coherencia, convertiremos todos los nombres de las columnas en cadenas más adelante.

'''
Seleccionar fila
Hay 2 formas principales de seleccionar filas:

    df.loc[label] # filtra por las etiquetas del índice/columna
    df.iloc[index] # filtra por las posiciones del índice/columna
    
Antes de continuar, observe que el índice predeterminado del conjunto de datos es un rango numérico de 0 a 194. Esto hace que sea muy difícil realizar una consulta 
por un país específico. Por ejemplo, para buscar datos sobre Japón, necesitamos conocer el valor del índice correspondiente.

Esto se puede solucionar muy fácilmente configurando la columna 'País' como índice usando el método set_index().
'''
df_can.set_index('Pais', inplace=True)
# consejo: se restablece lo contrario de set. Entonces, para restablecer el índice, podemos usar df_can.reset_index()
print(df_can.head(2))
#opcional: para eliminar el nombre del índice
df_can.index.name = None
'''
Ejemplo: veamos el número de inmigrantes de Japón (fila 87) para los siguientes escenarios: 
    1. Los datos de la fila completa (todas las columnas) 
    2. Para el año 2013 
    3. Para los años 1980 a 1985
'''
# 1. los datos de la fila completa (todas las columnas)
print(df_can.loc['Japan'])
#Métodos alternativos
df_can.iloc[87]
df_can[df_can.index == 'Japan']

# 2. Para el año 2013 
print(df_can.loc['Japan', 2013])
'''
Método alternativo
2013 esta en la última columna y su posición es la 36
'''
df_can.iloc[87, 36]

#3. Para los años 1980 a 1985
print(df_can.loc['Japan', [1980, 1981, 1982, 1983, 1984, 1985]])
#Método alternativo
df_can.iloc[87, [3,4,5,6,7,8]]
'''
Los nombres de columnas que son números enteros (como los años) pueden generar cierta confusión. Por ejemplo, cuando hacemos referencia al año 2013, 
uno podría confundirlo con el índice posicional número 2013.

Para evitar esta ambigüedad, conviertamos los nombres de las columnas en cadenas: '1980' a '2013'.
'''
df_can.columns = list(map(str, df_can.columns))
#Dado que convertimos los años a cadena, declaremos una variable que nos permitirá invocar fácilmente el rango completo de años:
# útil para trazar más adelante
years = list(map(str, range(1980,2014)))
print(years)

'''
Filtrado basado en un criterio.

Para filtrar el marco de datos según una condición, simplemente pasamos la condición como un vector booleano.

Por ejemplo, filtremos el marco de datos para mostrar los datos de los países asiáticos (AreaName = Asia).
'''
#1. Creamos la condicion Booleana
condicion = df_can['Continente'] == 'Asia'
print(condicion)
#2. Pasamos esta condición al marco de datos.
#df_can[condicion]
df_can[condicion]
print(df_can[condicion])

# podemos pasar múltiples criterios en la misma línea.
# filtremos por AreaNAme = Asia y RegName = Sur de Asia
condicion2 = df_can['Region'] =='Southern Asia'
print(df_can[condicion & condicion2])

# nota: cuando se utilizan los operadores 'y' y 'o', pandas requiere que usemos '&' y '|' en lugar de 'y' y 'o'
# no olvides encerrar las dos condiciones entre paréntesis
# Antes de continuar: revisemos los cambios que hemos realizado en nuestro marco de datos.
print('Dimension de los datos', df_can.shape)
print(df_can.columns)
print(df_can.head(2))

'''
Visualización de datos usando Matplotlib
Matplotlib: biblioteca de visualización estándar de Python
La biblioteca de trazado principal que exploraremos en el curso es Matplotlib. Como se menciona en su sitio web:

Matplotlib es una biblioteca de trazado 2D de Python que produce cifras de calidad de publicación en una variedad de formatos impresos y entornos interactivos en todas las plataformas. Matplotlib se puede utilizar en scripts de Python, el shell de Python e IPython, el cuaderno jupyter, servidores de aplicaciones web y cuatro kits de herramientas de interfaz gráfica de usuario.

Si aspira a crear una visualización impactante con Python, Matplotlib es una herramienta esencial que debe tener a su disposición.

Matplotlib.Pyplot
Uno de los aspectos centrales de Matplotlib es matplotlib.pyplot. Es la capa de secuencias de comandos de Matplotlib que estudiamos en detalle en los videos sobre Matplotlib. 
Recuerde que es una colección de funciones de estilo de comando que hacen que Matplotlib funcione como MATLAB. Cada función de pyplot realiza algún cambio en una figura: por ejemplo, crea una figura, crea un área de trazado en una figura, traza algunas líneas en un área de trazado, decora el trazado con etiquetas, etc. En esta práctica de laboratorio, trabajaremos con las secuencias de comandos. capa para aprender a generar gráficos de líneas. En laboratorios futuros, también trabajaremos con la capa Artista para experimentar de primera mano en qué se diferencia de la capa de secuencias de comandos.

Comencemos importando matplotlib y matplotlib.pyplot de la siguiente manera:

import matplotlib as mpl
import matplotlib.pyplot as plt

*opcional: aplique un estilo a Matplotlib.
'''
print(plt.style.available)
mpl.style.use[['fivethirtyeight']]#Ponemos el estilo fivethirtyeight

'''
Trazando en pandas
Afortunadamente, pandas tiene una implementación incorporada de Matplotlib que podemos usar. Trazar en pandas es tan simple como agregar un método .plot() a una serie o marco de datos.

Documentación:

Trazar con series -> https://pandas.pydata.org/pandas-docs/stable/reference/index.html
Trazar con marcos de datos -> https://pandas.pydata.org/pandas-docs/stable/reference/index.html
Potenciómetros de línea (serie/marco de datos) 
¿Qué es un diagrama lineal y por qué utilizarlo?

Un gráfico de líneas o diagrama de líneas es un tipo de gráfico que muestra información como una serie de puntos de datos llamados "marcadores" conectados por segmentos de línea recta. Es un tipo básico de gráfico común en muchos campos. Utilice un gráfico de líneas cuando tenga un conjunto de datos continuo. Son más adecuados para visualizaciones de datos basadas en tendencias durante un período de tiempo.

Comencemos con un estudio de caso:

En 2010, Haití sufrió un catastrófico terremoto de magnitud 7,0. El terremoto causó una devastación generalizada y pérdida de vidas y alrededor de tres millones de personas se vieron
afectadas por este desastre natural. Como parte del esfuerzo humanitario de Canadá, el Gobierno de Canadá intensificó sus esfuerzos para aceptar refugiados de Haití. 
Podemos visualizar rápidamente este esfuerzo usando un diagrama de líneas:

Pregunta: Trace un gráfico lineal de la inmigración desde Haití usando df.plot().

Primero, extraeremos la serie de datos de Haití.
'''