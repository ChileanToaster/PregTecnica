# PregTecnica

## Pregunta 1: Modelos

### Activo:

- Nombre del activo (EEUU, Europa, Japón, etc.)

### PrecioActivo:

- Nombre del activo

- Fecha del precio

- Precio del activo en dada fecha


### Portafolio

- Nombre del portafolio (Portafolio1, Portafolio2)

### ActivoPortafolio

- Portafolio (Llave foránea)

- Activo (Llave foránea)

- Cantidad que posee el portafolio del activo dado

## Pregunta 1: Decisiones

- Se decidió no guardar el peso de un activo dado en un portafolio ni el valor total del portafolio, pues se planea calcular estos valores dinámicamente.


## Pregunta 2: Features

- La función para poblar la base de datos se encuentra en "/cargar_datos/management/commmands/cargar_datos_de_xlsx.py", específicamente en el método 'handle'

- Para ejecutar el comando y poblar la base de datos posicionarse en el directorio "/Portfolio/portfolio" y ejecutar en la linea de comandos

```console
python ./manage.py cargar_datos_de_xlsx
```

- Notar que el comando cargar_datos_de_xlsx recibe opcionalmente el archivo excel a usar para poblar la base de datos, y por defecto usa el archivo datos.xlsx dado, ubicado en /cargar_datos/datos/

## Pregunta 2: Decisiones

- Tal como se señaló en [Pregunta 1: Decisiones](#pregunta-1-decisiones), se planea calcular el peso de un activo en un portafolio dinámicamente, por lo que la base de datos poblada solo tiene los dos portafolios, los 17 activos y sus historiales de precios. En la pregunta 3 se calculará la cantidad de un activo que posee cada portafolio y se terminará de poblar la base de datos.

## Pregunta 3: Features

- La función que calcula las cantidades para cada activo se encuentra en "/portafolios/management/commands/calcular_cantidades_activos.py", específicamente en el método 'handle'

- Para ejecutar el comando y calcular las cantidades de cada activo por portafolio posicionarse en el directorio "/Portfolio/portfolio" y ejecutar en la linea de comandos

```console
python .\manage.py calcular_cantidades_activos 1000000000
```

- Notar que el comando recibe el valor inicial a usar, que es global para los portafolios. Además, recibe opcionalmente la ruta al archivo excel a usar para ver los pesos, usando datos.xlsx por defecto. Este archivo debe seguir el mismo formato que el datos.xlsx dado.

- Al terminar, el comando imprime cada portafolio y la cantidad de cada activo que posee.
