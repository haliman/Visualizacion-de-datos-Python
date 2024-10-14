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
    figsize=(13, 5)
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
    figsize=(13, 5)
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
ax = df_top5.plot(kind='area', alpha=0.35, figsize=(13, 5))

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
    figsize=(13,5)
)
plt.title('Tendencia de la inmigracion de los 5 paises que menos han contribuido')
plt.ylabel('Numero de inmigrantes')
plt.xlabel('Años')

plt.show()

'''
**Pregunta**: Utilice la capa de artista para crear un gráfico de área no apilada de los 5 países que menos contribuyeron a la inmigración a Canadá **de** 1980 a 2013.
Utilice un valor de transparencia de 0,55.
'''
ax = df_least_5.plot(
    kind='area',
    alpha=0.55,
    figsize=(13,5)
)
ax.set_title('Tendencia de la inmigracion de los 5 paises que menos han contribuido')
ax.set_ylabel('Número de inmigrantes')
ax.set_xlabel('Años')
plt.show()

'''
Histogramas

Un histograma es una forma de representar la distribución de *frecuencia* de un conjunto de datos numéricos. La forma en que funciona es dividir el eje x en *bins*,
asigna cada punto de datos de nuestro conjunto de datos a un bin y luego cuenta el número de puntos de datos que se han asignado a cada bin. 
Entonces, el eje y es la frecuencia o el número de puntos de datos en cada contenedor. Tenga en cuenta que podemos cambiar el tamaño del contenedor y, por lo general,
es necesario modificarlo para que la distribución se muestre bien.

**Pregunta:** ¿Cuál es la distribución de frecuencia del número (población) de nuevos inmigrantes de varios países a Canadá en 2013?

Antes de continuar con la creación del gráfico del histograma, primero examinemos los datos divididos en intervalos. Para hacer esto, usaremos el método
`histrogram` de **Numpy** para obtener los rangos de contenedores y los recuentos de frecuencia de la siguiente manera:
'''
count, bin_edges = np.histogram(df_can['2013'])
print(count)# recuento de frecuencia
print(bin_edges) # rangos de contenedores, predeterminado = 10 contenedores

'''
De forma predeterminada, el método "histrogram" divide el conjunto de datos en 10 contenedores. La siguiente figura resume los rangos de bins y la distribución de frecuencia 
de la inmigración en 2013. Podemos ver eso en 2013:
* 178 países contribuyeron entre 0 y 3412,9 inmigrantes. 
* 11 países aportaron entre 3412,9 y 6825,8 inmigrantes
* 1 país aportó entre 6285,8 y 10238,7 inmigrantes, y así sucesivamente.

 https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%202/images/Mod2Fig1-Histogram.jpg
 
 
Podemos realizar el grafico fácilmente de esta distribución pasando `kind=hist` a `plot()`.
'''
df_can['2013'].plot(
    kind='hist',
    figsize=(8,5)
)
plt.title('Histograma de la inmigración de los 195 países en 2013')
plt.ylabel('Número de países')
plt.xlabel('Número de inmigrantes')
plt.show()

'''
En el gráfico anterior, el eje x representa el rango poblacional de inmigrantes en intervalos de 3412,9. El eje y representa el número de países que contribuyeron a la población 
antes mencionada. 

Observe que las etiquetas del eje x no coinciden con el tamaño del contenedor. Esto se puede solucionar pasando una palabra clave `xticks` que contenga la lista de tamaños de 
contenedores, de la siguiente manera:
'''
count, bin_edges = np.histogram(df_can['2013'])

df_can['2013'].plot(
    kind='hist',
    figsize=(8,5),
    xticks=bin_edges
)
plt.title('Histograma de la inmigración de los 195 países en 2013')
plt.ylabel('Número de países')
plt.xlabel('Número de inmigrantes')
plt.show()

'''
*Nota al margen:* Podríamos usar `df_can['2013'].plot.hist()`, en vez de usar `some_data.plot(kind='type_plot',...)` es equivalente a `some_data.plot.type_plot(...)`. 
Es decir, pasar el tipo de gráfico como argumento o método se comporta igual. 

Consulte la documentación de *pandas* para obtener más información http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.plot.html.


También podemos trazar múltiples histogramas en el mismo gráfico. Por ejemplo, intentemos responder las siguientes preguntas usando un histograma.

**Pregunta**: ¿Cuál es la distribución de la inmigración para Dinamarca, Noruega y Suecia durante los años 1980 - 2013?
'''
df_can.loc[['Denmark', 'Norway', 'Sweden'], years].plot.hist()
plt.show()

'''
¡Eso no se ve bien! 

No te preocupes, a menudo te encontrarás con situaciones como ésta al crear tramas. La solución suele radicar en cómo está estructurado el conjunto de datos subyacente.

En lugar de trazar la distribución de frecuencia de la población de los 3 países, *pandas* trazó la distribución de frecuencia de la población para los "años".

Esto se puede solucionar fácilmente transponiendo primero el conjunto de datos y luego graficando como se muestra a continuación.
'''
df_t = df_can.loc[['Denmark', 'Norway', 'Sweden'], years].transpose()
df_t.plot(
    kind='hist',
    figsize=(10,6)
)
plt.title('Histograma de la inmigración de Dinamarca, Noruega y Suiza desde 1980 a 2013')
plt.ylabel('Número de años')
plt.xlabel('Número de inmigrantes')
plt.show()

'''
Hagamos algunas modificaciones para mejorar el impacto y la estética de la trama anterior:
* aumentar el tamaño del contenedor a 15 pasando el parámetro `bins`;
* establezca la transparencia al 60% pasando el parámetro "alfa";
* etiquetar el eje x pasando el parámetro `x-label`;
* cambiar los colores de los gráficos pasando el parámetro `color`.
'''
count, bin_edges = np.histogram(df_t, 15)

df_t.plot(
    kind='hist',
    bins=15,
    alpha=0.6,
    xticks=bin_edges,
    color=['coral', 'darkslateblue', 'mediumseagreen']
)
plt.title('Histograma de la inmigración de Dinamarca, Noruega y Suiza desde 1980 a 2013')
plt.ylabel('Número de años')
plt.xlabel('Número de inmigrantes')
plt.show()
'''
Consejo:
Para obtener una lista completa de los colores disponibles en Matplotlib, ejecute el siguiente código en su shell de Python:
```python
import matplotlib
for name, hex in matplotlib.colors.cnames.items():
    print(name, hex)
```
Si no queremos que los gráficos se superpongan entre sí, podemos apilarlos usando el parámetro "stacked". También ajustemos las etiquetas mínima y máxima del eje x
para eliminar el espacio adicional en los bordes del gráfico. Podemos pasar una tupla (min,max) usando el parámetro `xlim`, como se muestra a continuación.
'''
count, bin_edges = np.histogram(df_t, 15)
min = bin_edges[0] - 10
max = bin_edges[-1] +10

df_t.plot(
    kind='hist',
    bins=15,
    alpha=0.6,
    xticks=bin_edges,
    color=['coral', 'darkslateblue', 'mediumseagreen'],
    stacked=True,
    xlim=(min, max)
)
plt.title('Histograma de la inmigración de Dinamarca, Noruega y Suiza desde 1980 a 2013')
plt.ylabel('Número de años')
plt.xlabel('Número de inmigrantes')
plt.show()
'''

**Pregunta**: ¿Utiliza la capa de secuencias de comandos para mostrar la distribución de la inmigración para Grecia, Albania y Bulgaria durante los años 1980 - 2013? 
Utilice un gráfico superpuesto con 15 contenedores y un valor de transparencia de 0,35.
'''
df_cof = df_can.loc[['Greece', 'Albania', 'Bulgaria'], years].transpose()

count, bin_edges = np.histogram(df_cof, 15)
df_cof.plot(
    kind='hist',
    figsize=(10,6),
    bins=15,
    alpha=0.35,
    xticks=bin_edges,
    color=['coral', 'darkslateblue', 'mediumseagreen'],
)
plt.title('Histograma de la inmigración de Grecia, Albania y Bulgaria desde 1980 a 2013')
plt.ylabel('Número de años')
plt.xlabel('Número de inmigrantes')
plt.show()

'''
Gráficos de barras (marco de datos)

Un diagrama de barras es una forma de representar datos donde la *longitud* de las barras representa la magnitud/tamaño de la característica/variable.
Los gráficos de barras suelen representar variables numéricas y categóricas agrupadas en intervalos. 

Para crear un gráfico de barras, podemos pasar uno de dos argumentos mediante el parámetro `kind` en `plot()`:

* `kind=bar` crea un gráfico de barras *vertical*
* `kind=barh` crea un gráfico de barras *horizontal*

**Gráfico de barras verticales**

En los gráficos de barras verticales, el eje x se utiliza para etiquetar y la longitud de las barras en el eje y corresponde a la magnitud de la variable
que se está midiendo. Los gráficos de barras verticales son particularmente útiles para analizar datos de series de tiempo. Una desventaja es que carecen
de espacio para etiquetas de texto al pie de cada barra.

**Empecemos analizando el efecto de la crisis financiera de Islandia:**

La crisis financiera islandesa de 2008-2011 fue un importante acontecimiento económico y político en Islandia. En relación con el tamaño de su economía, 
el colapso bancario sistémico de Islandia fue el mayor experimentado por cualquier país en la historia económica. La crisis provocó una grave depresión 
económica en 2008-2011 y un importante malestar político.

**Pregunta:** Comparemos el número de inmigrantes islandeses (país = 'Islandia') en Canadá desde el año 1980 al 2013.
'''
df_iceland = df_can.loc['Iceland', years]

df_iceland.plot(
    kind='bar', 
    figsize=(10, 6)
    )

plt.xlabel('Año')
plt.ylabel('Número de inmigrantes')
plt.title('Inmigración de islandia a canada desde 1980 a 2013')
plt.show()

'''
El gráfico de barras de arriba muestra el número total de inmigrantes desglosado por año. Podemos ver claramente el impacto de la crisis financiera; 
El número de inmigrantes a Canadá comenzó a aumentar rápidamente después de 2008. 

Anotemos esto en el gráfico usando el método `annotate` de la **scripting layer** o la **pyplot interface**. Pasaremos los siguientes parámetros:
- `s`: str, el texto de la anotación.
- `xy`: Tupla que especifica el punto (x,y) a anotar (en este caso, el punto final de la flecha).
- `xytext`: Tupla que especifica el punto (x,y) para colocar el texto (en este caso, punto inicial de la flecha).
- `xycoords`: el sistema de coordenadas en el que se proporciona xy - 'data' utiliza el sistema de coordenadas del objeto que se está anotando (predeterminado).
- `arrowprops`: Toma un diccionario de propiedades para dibujar la flecha:
    - `arrowstyle`: especifica el estilo de la flecha, `'->'` es la flecha estándar.
    - `connectionstyle`: Especifica el tipo de conexión. `arc3` es una línea recta.
    - `color`: especifica el color de la flecha.
    - `lw`: Especifica el ancho de la línea.

Le recomiendo que lea la documentación de Matplotlib para obtener más detalles sobre las anotaciones: 
http://matplotlib.orsg/api/pyplot_api.html#matplotlib.pyplot.annotate.
'''
df_iceland.plot(
    kind='bar', 
    figsize=(10, 6), 
    rot=90
    ) 

plt.xlabel('Año')
plt.ylabel('Número de inmigrantes')
plt.title('Inmigración de islandia a canada desde 1980 a 2013')

plt.annotate('', # s: str. Lo dejaré en blanco para no seguir
             xy=(32, 70), # coloque la cabeza de la flecha en el punto (año 2012, pop 70)
             xytext=(28,20), # coloque la base de la flecha en el punto (año 2008, pop 20)
             xycoords=('data'), # utilizará el sistema de coordenadas del objeto que se está anotando
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
             )

plt.show()

'''
También anotamos un texto para pasar sobre la flecha.  Pasaremos los siguientes parámetros adicionales:
- `rotación`: ángulo de rotación del texto en grados (en el sentido contrario a las agujas del reloj)
- `va`: alineación vertical del texto [‘centro’ | 'arriba' | 'abajo' | 'base']
- `ha`: alineación horizontal del texto [‘centro’ | 'correcto' | 'izquierda']
'''
df_iceland.plot(kind='bar', figsize=(10, 6), rot=90)

plt.xlabel('Año')
plt.ylabel('Número de inmigrantes')
plt.title('Inmigración de islandia a canada desde 1980 a 2013')

# Annotate arrow
plt.annotate('',  
             xy=(32, 70),
             xytext=(28, 20),
             xycoords='data',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='blue', lw=2)
             )

# Annotate Text
plt.annotate('2008 - 2011 Crisis financiera',  
             xy=(28, 30),
             rotation=72.5,
             va='bottom',
             ha='left',
             )

plt.show()

'''
**Gráfica de barras horizontales**

A veces es más práctico representar los datos horizontalmente, especialmente si necesitas más espacio para etiquetar las barras. En los gráficos de barras horizontales,
el eje y se utiliza para etiquetar y la longitud de las barras en el eje x corresponde a la magnitud de la variable que se está midiendo. Como verá, hay más espacio en el eje
y para etiquetar variables categóricas.


**Pregunta:** Utilizando el script más adelante y el conjunto de datos `df_can`, cree un diagrama de barras *horizontal* que muestre el número *total* de inmigrantes a Canadá
de los 15 principales países, para el período 1980 - 2013. Etiquete cada país con el recuento total de inmigrantes.
'''
df_can.sort_values(by='Total', ascending=True, inplace=True)
df_top15 = df_can['Total'].tail(15)

'''
Paso 2: Trazar gráfica:
   1. Utilice `kind='barh'` para generar un gráfico de barras con barras horizontales.
   2. Asegúrate de elegir un buen tamaño para el gráfico, etiquetar tus ejes y darle un título al gráfico.
   3. Recorra los países y anote la población inmigrante utilizando la función de anotación de la interfaz de secuencias de comandos.
'''

df_top15.plot(
    kind='barh', 
    figsize=(12, 12), 
    color='steelblue'
    )
plt.xlabel('Número de inmigrantes')
plt.title('Top 15 de los países con más inmigración a Canada entre 1980 - 2013')

for index, value in enumerate(df_top15): 
    label = format(int(value), ',') 
    plt.annotate(
        label, 
        xy=(value - 47000, index - 0.10), 
        color='white'
        )

plt.show()