# Descarga y preparación de datos
'''
Lo primero que haremos será instalar **openpyxl** (anteriormente **xlrd**), un módulo que *pandas* requiere para leer archivos de Excel.

Importar módulos primarios. Lo primero que haremos será importar dos módulos de análisis de datos clave: `pandas` y `numpy`.
'''
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#Descargue el conjunto de datos de inmigración canadiense y léalo en un marco de datos *pandas*.
df_can = pd.read_excel(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Canada.xlsx',
    sheet_name = 'Canada by Citizenship',
    skiprows = range(20),
    skipfooter = 2
)

#Echemos un vistazo a los primeros cinco elementos de nuestro conjunto de datos.
print(df_can.head())

'''
Limpiar datos. Haremos algunas modificaciones al conjunto de datos original para facilitar la creación de nuestras visualizaciones. 
Consulte el laboratorio de "Introducción a Matplotlib y diagramas de líneas" para obtener una descripción racional y detallada de los cambios.

1. Limpie el conjunto de datos para eliminar las columnas que no nos son informativas para la visualización (p. ej., Tipo, ÁREA, REG).
Observe cómo las columnas Tipo, Cobertura, ÁREA, REG y DEV se eliminaron del marco de datos.
2. Cambie el nombre de algunas de las columnas para que tengan sentido.
Observe cómo los nombres de las columnas ahora tienen mucho más sentido, incluso para un extraño.
3. Para mantener la coherencia, asegúrese de que todas las etiquetas de las columnas sean de tipo cadena.
Observe cómo la línea de código anterior devolvió *False* cuando probamos si todas las etiquetas de las columnas son del tipo **string**. Así que cambiémoslos todos al tipo **string**.
4. Establezca el nombre del país como índice: útil para buscar países rápidamente utilizando el método .loc.
Observe ahora que los nombres de los países ahora sirven como índices.
5. Añadir total columnas.
Ahora el marco de datos tiene una columna adicional que presenta el número total de inmigrantes de cada país en el conjunto de datos de 1980 a 2013. Entonces, si imprimimos la dimensión de los datos.
Entonces ahora nuestro marco de datos tiene 38 columnas en lugar de las 37 columnas que teníamos antes.
'''
df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)
df_can.rename(columns={'OdName':'Pais', 'AreaName':'Continente', 'RegName':'Region'}, inplace=True)
print(all(isinstance(column, str) for column in df_can.columns))
df_can.columns = list(map(str, df_can.columns))
df_can.set_index('Pais', inplace=True)
df_can['Total'] = df_can.sum(axis=1, numeric_only=True)
print('DImension de datos', df_can.shape)
# finalmente, creemos una lista de años desde 1980 - 2013
# esto será útil cuando comencemos a trazar los datos
years = list(map(str, range(1980, 2014)))

'''
Visualización de datos usando Matplotlib

importamos las librerias de matplotlib

import matplotlib as mpl
import matplotlib.pyplot as plt

Grafica de Area

En el último módulo, creamos un gráfico de líneas que visualizaba los 5 países principales que aportaron la mayor cantidad de inmigrantes a Canadá entre 1980 y 2013. Con una pequeña modificación en el código,
podemos visualizar este gráfico como un gráfico acumulativo, también conocido como gráfico **Gráfico de líneas apiladas** o **Gráfico de áreas**.
'''
df_can.sort_values(['Total'], ascending=False, axis=0, inplace=True)
#Cogemos las 5 primears entradas
df_top5 = df_can.head()
# transponer el marco de datos
df_top5 = df_top5[years].transpose()
print(df_top5.head())

'''
Los gráficos de área se apilan de forma predeterminada. Y para producir un gráfico de áreas apiladas, cada columna debe tener todos valores positivos o todos negativos 
(cualquier `NaN`, es decir, no un número, los valores predeterminados serán 0). Para producir un gráfico no apilado, establezca el parámetro "apilado(stacked)" en el valor "Falso".
'''
df_top5.index = df_top5.index.map(int)
df_top5.plot(
    kind='area',
    stacked=False,
    figsize=(15, 5)
)
plt.title('Tendencia de inmigración de los 5 principales países')
plt.ylabel('Número de inmigrantes')
plt.xlabel('Años')

plt.show()
#El gráfico no apilado tiene una transparencia predeterminada (valor alfa) de 0,5. Podemos modificar este valor pasando el parámetro `alpha`.

df_top5.plot(
    kind='area',
    alpha=0.25,
    stacked=False,
    figsize=(15, 5)
)
plt.title('Tendencia de inmigración de los 5 principales países')
plt.ylabel('Número de inmigrantes')
plt.xlabel('Años')

plt.show()

'''
### Dos tipos de trazado

Como comentamos en las conferencias en video, hay dos estilos/opciones para trazar con `matplotlib`: trazar usando la capa Artista y trazar usando la capa de secuencias de comandos.

**Opción 1: capa de secuencias de comandos (método de procedimiento): usar matplotlib.pyplot como 'plt' **

Puede usar `plt`, es decir, `matplotlib.pyplot` y agregar más elementos llamando a diferentes métodos de forma procesal; 
por ejemplo, `plt.title(...)` para agregar un título o `plt.xlabel(...)` para agregar una etiqueta al eje x.
python
    # Option 1: This is what we have been using so far
    df_top5.plot(kind='area', alpha=0.35, figsize=(20, 10)) 
    plt.title('Immigration trend of top 5 countries')
    plt.ylabel('Number of immigrants')
    plt.xlabel('Years')
    
**Opción 2: Capa de artista (método orientado a objetos): usar una instancia `Axes` de Matplotlib (preferido) **

Puede utilizar una instancia de `Axes` de su gráfico actual y almacenarla en una variable (por ejemplo, `ax`). 
Puedes agregar más elementos llamando a métodos con un pequeño cambio en la sintaxis (agregando "`set_`" a los métodos anteriores). 
Por ejemplo, use `ax.set_title()` en lugar de `plt.title()` para agregar un título, o `ax.set_xlabel()` en lugar de `plt.xlabel()` para agregar una etiqueta al eje x.

Esta opción a veces es más transparente y flexible para usar en gráficos avanzados (en particular cuando se tienen múltiples gráficos, como verá más adelante). 

En este curso, nos ceñiremos a la **capa de secuencias de comandos**, excepto para algunas visualizaciones avanzadas en las que necesitaremos usar la **capa de artista** para manipular aspectos avanzados de las tramas.

'''
ax = df_top5.plot(kind='area', alpha=0.35, figsize=(15, 5))

ax.set_title('Immigration Trend of Top 5 Countries')
ax.set_ylabel('Number of Immigrants')
ax.set_xlabel('Years')
plt.show()
'''
**Pregunta**: Utilice la capa de secuencias de comandos para crear un gráfico de áreas apiladas de los 5 países que menos contribuyeron a la inmigración a Canadá **de** 1980 a 2013. 
Utilice un valor de transparencia de 0,45.
'''
df_least_5 = df_can.tail(5)
df_least_5 = df_least_5[years].transpose()
df_least_5.index = df_least_5.index.map(int)
df_least_5.plot(
    kind='area',
    alpha=0.45,
    stacked=False,
    figsize=(15,5)
)
plt.title('Tendencia de la inmigracion de los 5 paises que menos han contribuido')
plt.ylabel('Numero de inmigrantes')
plt.xlabel('Años')

plt.show()

'''
**Pregunta**: Utilice la capa de artista para crear un gráfico de área no apilada de los 5 países que menos contribuyeron a la inmigración a Canadá **de** 1980 a 2013. Utilice un valor de transparencia de 0,55.
'''
ax = df_least_5.plot(
    kind='area',
    alpha=0.55,
    figsize=(15,5)
)
ax.set_title('Tendencia de la inmigracion de los 5 paises que menos han contribuido')
ax.set_ylabel('Número de inmigrantes')
ax.set_xlabel('Años')
plt.show()