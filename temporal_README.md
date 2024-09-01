# ST0263 Tópicos en telemática

## Estudiantes:
- Luisa María Álvarez García, lmalvarez8@eafit.edu.co
- Sebastián Restrepo Ortiz, srestrep74@eafit.edu.co

## Profesor: 
- Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co

## Descripción

Para el presente reto se implemento una red P2P mediante el protocolo Chord DHT. Chord es un protocolo P2P estructurado que organiza los nodos en un anillo lógico. Cada nodo tiene un identificador único generado mediante hashing (por ejemplo, SHA-1). Los archivos (o recursos) se almacenan en los nodos, y la búsqueda de archivos se realiza mediante un proceso de búsqueda en el anillo utilizando las "finger tables" de los nodos para acelerar el proceso.

### Caracteristicas principales
- Nodos P2P: Cada nodo en la red es responsable de almacenar un rango de claves (hashes) y de proporcionar servicios para la inserción, búsqueda y recuperación de archivos.
- Finger Table: Cada nodo mantiene una finger table que optimiza la búsqueda de nodos responsables de claves específicas, reduciendo la complejidad de las búsquedas a $𝑂(log_{2}𝑁)$, donde $𝑁$ es el número de nodos.
- Responsabilidad de los Nodos: Cada nodo es responsable de un intervalo de claves en el espacio de hash, y cualquier archivo que se hash en ese intervalo es responsabilidad de ese nodo.
- gRPC para Comunicación: Se utiliza gRPC para manejar la comunicación entre nodos, permitiendo que los nodos envíen y reciban solicitudes de búsqueda y transferencia de archivos.

### 1.1. Aspectos implementados

1. **Estructura básica de nodos Chord**
   - Implementación de la clase `Node` con funcionalidades clave de Chord.
   - Manejo de ID de nodos y recursos mediante hashing SHA-1.

2. **Comunicación entre nodos con gRPC**
   - Definición de servicios gRPC para operaciones Chord (FindSuccessor, GetPredecessor, etc.).
   - Implementación de servidor gRPC para manejar solicitudes entrantes.

3. **Operaciones Chord fundamentales**
   - Búsqueda de sucesor (`find_successor`)
   - Mantenimiento de tabla de dedos (`fix_fingers`)
   - Estabilización de la red (`stabilize`)
   - Unión de nodos a la red (`join`)

4. **Almacenamiento y búsqueda de recursos**
   - Métodos para almacenar recursos localmente (`store_local`)
   - Búsqueda de recursos en la red (`lookup`)

5. **Manejo de desconexiones de nodos**
   - Detección de nodos caídos mediante ping
   - Actualización de tabla de dedos cuando se detectan nodos desconectados
   - Procedimiento para que un nodo abandone la red de manera ordenada

6. **Interfaz de usuario interactiva**
   - Menú para interactuar con el nodo (almacenar recursos, buscar recursos, imprimir tabla de dedos)
   - Opción para que un nodo abandone la red

7. **Containerización con Docker**
   - Dockerfile para empaquetar la aplicación y sus dependencias
   - Configuración para ejecutar nodos Chord en contenedores

8. **Manejo de errores y excepciones**
   - Tratamiento de errores de comunicación gRPC
   - Manejo de situaciones como nodos no disponibles o particiones de red

9. **Configuración flexible de nodos**
   - Posibilidad de iniciar nodos con diferentes IDs y direcciones
   - Opción para unirse a una red existente o iniciar una nueva


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Uno de los aspectos que no se implementó en la entrega del proyecto se refiere al almacenamiento de archivos en carpetas físicas dentro del sistema. En particular, se esperaba que la implementación permitiera que los archivos almacenados por cada nodo se gestionaran en directorios específicos en el sistema de archivos.

El objetivo era permitir que cada nodo tuviera su propio directorio físico para los archivos que almacena, facilitando así la organización y el acceso a dichos archivos a nivel del sistema operativo. Sin embargo, esta funcionalidad no se desarrolló en la medida esperada debido a la complejidad que implica modificar la estructura de almacenamiento a nivel de código para manejar directorios físicos.

La principal dificultad radica en la integración de la gestión de archivos en carpetas dentro del marco del sistema distribuido, lo que requirió un esfuerzo significativo en términos de diseño y programación. La falta de esta implementación limita la capacidad de organizar y acceder a los archivos de manera más estructurada y puede afectar la facilidad de mantenimiento y la eficiencia en el manejo de datos en el proyecto.

## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

#### Arquitectura DHT
Chord es un protocolo de red Peer-to-Peer (P2P) diseñado para facilitar la localización eficiente de datos en una red distribuida. Este protocolo implementa una Distributed Hash Table (DHT), que permite almacenar y recuperar datos sin necesidad de un servidor central. Chord es fundamental en sistemas distribuidos donde la escalabilidad y la robustez son esenciales, ya que permite la distribución y gestión de grandes volúmenes de datos como archivos entre múltiples nodos de manera descentralizada.

#### Estructura de la red
En Chord, los nodos están organizados en un anillo lógico, donde cada nodo es responsable de un segmento del espacio de claves. El espacio de claves es un rango de identificadores generados por una función hash, como SHA-1, que distribuye tanto los nodos como los datos en un espacio de identificadores de tamaño fijo, normalmente de $2^m$, donde m es el número de bits utilizados por la función hash. Cada clave se almacena en el primer nodo cuyo identificador es igual o superior al identificador de la clave, garantizando una distribución equitativa de los datos en la red.

#### Mecanismo de Busqueda
El proceso de búsqueda en Chord se realiza utilizando un algoritmo de búsqueda que, en promedio, encuentra el nodo responsable de una clave en O(log N) saltos, donde N es el número total de nodos en la red. Para mejorar la eficiencia de la búsqueda, cada nodo mantiene una tabla de enrutamiento llamada "Finger Table", que contiene hasta m entradas, apuntando cada una a un nodo a una distancia de potencia de dos en el anillo. Esta tabla permite que la búsqueda se realice en una cantidad de saltos logarítmica con respecto al tamaño de la red.

#### Operaciones Basicas
Las operaciones principales en Chord son la inserción y recuperación de datos, así como la gestión de la unión y salida de nodos en la red:

Inserción de Datos: Un nodo que desee insertar un dato en la DHT primero calcula el identificador de la clave del dato utilizando la función hash. Luego, localiza el nodo correspondiente en el anillo y almacena el dato en dicho nodo.

Recuperación de Datos: Para recuperar un dato, se realiza una búsqueda similar, utilizando el algoritmo de lookup para localizar el nodo que almacena la clave del dato solicitado.

Unión y Salida de Nodos: Cuando un nodo se une a la red, Chord redistribuye las claves que estaban asignadas a otros nodos para mantener el equilibrio en la red. De manera similar, cuando un nodo sale de la red, sus claves se reasignan a su sucesor, y las tablas de enrutamiento de los nodos afectados se actualizan en consecuencia.

#### Manejo de Fallas
Chord maneja fallos mediante la replicación de claves en múltiples nodos sucesores, asegurando que, en caso de fallo de un nodo, los datos aún estén accesibles en la red. Además, los nodos supervisan a sus vecinos para detectar fallos y actualizar sus tablas de enrutamiento, lo que permite que la red continúe operando normalmente a pesar de la falla de algunos nodos.

![image](https://github.com/user-attachments/assets/ec2e5b4c-9e9b-4ef5-ae84-9faedaf4d83a)


### Diagrama de Secuencias
![Diagrama de Secuencias Chord DHT](https://www.planttext.com/api/plantuml/png/fLPDRzim3BtxLn0znK3MxLmWGu6Y6J84sT2ikmn3eCPq8yILF4bEb_twKVANP2UEr_MGHZJvI3u-qRdLXYbJl6GHsngfu56ZYd8oyItFcJ1mjP89NW7JOB-4Z-vsKYMmHdNWszB7MIf3wBikjblKcb8qW8sfZ_nLOO9TVy_e8gBPp3s4EuNCS2c0YGG-IowuU0QpGrYXUPLg3xDP5DdEuDt7Ck86rhRlyZ0HzBdXoHHOaYZ2tvWTrnjhRKsIy9IpnP6BQg4MWXlEClw7e3oKAQHK1mKPzfGHKjwMFmLTznv7B3EmIA4gWcg53n7GNoUBxQjfQBAIWWh1J6FW6r3Q2vfpaJGU3_YhG6seubcLEeuTLeX1eFvG2JD06GiQO9merFvRY5Jw19ufPp02HJ8mdhaR27op0nbmyuJsladlv4QgUUBaKyhDokeSyxKdQU8J6WynZYuH7Fh3vFubDySu6asX9pIdQl_S47MHrb4evxfVISFJevLfXTPSCVUbZh_CnMYWI-mu4jqC7r3BGf7NbnoL6wG-lI2amjPviiVZ50uiA_eBeEEwb5kMPLIq9ZjxnXyK-XDcTR1ttu5heFfpAe6J926bSTkzHG6dLa2P9olXBr_-kLIlp2ve6rRTJ9Zu9x-fSPU_Ygv96GORDnDxPRlaBwNS5td8Ve_soibje1ORP0hE-mqykofkAAqfb83ljfLcYjVFw5gCHwpTclcomeRwu5XXZI6zZgl9E8TpYUy6nnA1aqgFGqlsVCG0PUL4wQOjaHr6l8hlVtDJFm-cjgENlhTsWhoT7mC4yvWdpA0dX7PfD6zRjpdQKxi-B7GNiZ-8CiNRCtG7r6-YlH9T8XhCGULL90JlZtzQwUCKMQRvtopZzqD7RQkQb0nJu-GbAlb4j-HkVyx-1G00)

## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

### Lenguaje de Programación
- Python 3.9.5

### Librerías y Paquetes Principales
- gRPC 1.54.0
  - Framework de RPC (Remote Procedure Call) de alto rendimiento, de código abierto, inicialmente desarrollado por Google.
- grpcio-tools 1.54.0
  - Herramientas para compilar archivos .proto de gRPC.
- protobuf 4.22.3
  - Librería para serialización de datos estructurados.

### Dependencias Adicionales
- threading (librería estándar de Python)
  - Para manejo de hilos y concurrencia.
- time (librería estándar de Python)
  - Para operaciones relacionadas con el tiempo.
- sys (librería estándar de Python)
  - Para interactuar con el intérprete de Python.

### Herramientas de Desarrollo
- Visual Studio Code 1.78.0
  - IDE principal utilizado para el desarrollo.
- Docker 20.10.21
  - Para containerización de la aplicación.

### Sistema Operativo
- Desarrollo realizado en Windows 10 Pro, versión 21H2

### Gestión de Paquetes
- pip 23.1.2
  - Gestor de paquetes de Python utilizado para instalar y manejar dependencias.

### Control de Versiones
- Git 2.40.1
  - Sistema de control de versiones.

### Archivos de Configuración
- requirements.txt
  - Archivo que lista todas las dependencias del proyecto.
- Dockerfile
  - Archivo para la creación de la imagen Docker del proyecto.

### Estructura del Proyecto
- server.py: Archivo principal que contiene la lógica del servidor y la interfaz de usuario.
- node.py: Implementación de la clase Node con la lógica de Chord.
- chord_pb2.py y chord_pb2_grpc.py: Archivos generados por gRPC a partir del archivo .proto.
- chord.proto: Definición de los servicios gRPC y mensajes.
- utils.py: Funciones de utilidad, como el hashing SHA-1.

### Notas de Versión
- Este proyecto fue desarrollado y probado con las versiones de software mencionadas arriba.
- Se recomienda usar las mismas versiones o versiones compatibles para evitar problemas de incompatibilidad.


## Compilación y ejecución del proyecto

### Preparación del Entorno

1. Asegúrate de tener Python 3.9.5 o superior instalado.
2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```
### Compilación de los Archivos Proto

Antes de ejecutar el proyecto, necesitas compilar los archivos .proto para generar los archivos Python necesarios para gRPC:
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chord.proto
```
Este comando generará los archivos `chord_pb2.py` y `chord_pb2_grpc.py`.

### Ejecución del Proyecto


Antes de realizar la ejecución del proyecto es importante realizar previamente la configuración del archivo config.py en el que se establece la configuración previa de cada uno de los nodos.

Aquí está un ejemplo de config.py y peer.py con correcciones sugeridas:
```
SOURCE_ADDRESS = "127.0.0.1:50051"  # IP para pruebas locales
TARGET_ADDRESS = ""  # Deja vacío si es el primer nodo
NODE_ID = 0
PORT = "127.0.0.1:50051"  # Dirección y puerto para IPv4
```
Para ejecutar un nodo Chord:

```
python peer.py
```
Recordar realizar la modificación del archivo de configuración cada vez, antes de ejecutar y agregar un nodo en la red.

### Ejecución con Docker

En caso de preferir usar Docker:

1. Actualización dee la lista de paquetes e instalación las actualizaciones disponibles:
   ```
   sudo apt-get update
   sudo apt-get upgrade -y
   ```
2. Instalación de Docker:
   ```
   sudo apt-get install -y docker.io
   ```
3. Habilitar y arrancar el servidor Docker:
   ```
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

Para los pasos siguientes es necesario ajustar los parámetros del archivo config.py, llenando los campos para poder asignar de manera estática los valores de la etructura nodo en cada caso.

4. Creación de la imagen del archivo Dockerfile.

  ```
   docker build -t <nombre-de-la-imagen> .
   ```
5. Creación del contenedor en el que correrá la imagen para cada nodo.

   ```
   sudo docker run -it -p <puerto-máquina-anfitriona>:<puerto-contenedor-docker> <nombre-de-la-imagen>
   ```

Para nodos adicionales, ajusta el puerto mapeado y los parámetros según sea necesario.

### Interacción con el Nodo

Una vez que el nodo esté en ejecución, seguirá las instrucciones en la consola para interactuar con él. Puedes almacenar recursos, buscar recursos, imprimir la tabla de dedos o salir del programa.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Detalles del desarrollo
### Servicios definidos
Este servidor Chord implementa una red distribuida utilizando el protocolo gRPC para la comunicación entre nodos. A continuación, se detalla la especificación completa de los servicios ofrecidos por esta implementación.

### 1. `FindSuccessor`

- **Método**: `FindSuccessor`
- **Tipo**: RPC
- **Descripción**: Encuentra el sucesor de un nodo dado un identificador.
- **Solicitudes**:
  - `FindSuccessorRequest`:
    - `id` (int32): El identificador del nodo cuyo sucesor se desea encontrar.
- **Respuestas**:
  - `NodeInfo`:
    - `id` (int32): Identificador del nodo sucesor.
    - `address` (string): Dirección del nodo sucesor.

### 2. `GetPredeccessor`

- **Método**: `GetPredecessor`
- **Tipo**: RPC
- **Descripción**: Obtiene la información del predecesor del nodo.
- **Solicitudes**:
  - `Empty`: No se requieren datos adicionales.
- **Respuestas**:
  - `NodeInfo`:
    - `id` (int32): Identificador del nodo predecesor.
    - `address` (string): Dirección del nodo predecesor.

### 3. `Notify`

- **Método**: `Notify`
- **Tipo**: RPC
- **Descripción**: Notifica al nodo sobre su nuevo predecesor.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nodo que está notificando.
       - `address` (string): Dirección del nodo que está notificando.
- **Respuestas**:
 - `Empty`: No se requieren datos adicionales.

### 4. `StoreResource`

- **Método**: `StoreResource`
- **Tipo**: RPC
- **Descripción**: Almacena un recurso en el DHT.
- **Solicitudes**:
    - `StoreRequest`:
       - `key` (string): Clave del recurso.
       - `value` (string):  Valor del recurso.
- **Respuestas**:
 - `Empty`: Confirmación de que el recurso ha sido almacenado.

### 5. `LookupResource`

- **Método**: `LookupResource`
- **Tipo**: RPC
- **Descripción**: Busca un recurso en el DHT utilizando una clave
- **Solicitudes**:
    - `LookupRequest`:
       - `key` (string): Clave del recurso a buscar.
- **Respuestas**:
    - `LookupRequest`:
       - `value` (string) : Valor asociado con la clave, o un mensaje de error si no se encuentra.

### 6. `UpdateSuccessor`

- **Método**: `UpdateSuccessor`
- **Tipo**: RPC
- **Descripción**: Actualiza la información sobre el sucesor del nodo.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nuevo sucesor.
       - `address` (string): Dirección del nuevo sucesor.
- **Respuestas**:
    - `Empty` : Confirmación de que la información ha sido actualizada.

### 7. `UpdatePredecessor`

- **Método**: `UpdatePredecessor`
- **Tipo**: RPC
- **Descripción**: Actualiza la información sobre el predecesor del nodo.
- **Solicitudes**:
    - `NodeInfo`:
       - `id` (int32): Identificador del nuevo predecesor.
       - `address` (string): Dirección del nuevo predecesor.
- **Respuestas**:
    - `Empty` : Confirmación de que la información ha sido actualizada.

## Detalles técnicos

### Arquitectura del Sistema
El sistema P2P basado en Chord con DHT se organiza en una red distribuida donde los nodos colaboran para almacenar y recuperar datos de manera eficiente. Cada nodo en la red tiene una identificación única y se comunica con otros nodos para mantener la consistencia de los datos y el enrutamiento dentro del anillo Chord.

### Componentes Técnicos
- **Nodo P2P:**

   Funcionalidad: Implementa la lógica de conexión, almacenamiento y recuperación de datos. Mantiene una tabla de enrutamiento para localizar otros nodos y gestionar la tabla de hash distribuida (DHT).
   Lenguaje/Framework: Dependiendo de la implementación, puede estar basado en Python, Java, C++, etc., con uso de bibliotecas para redes y serialización de datos.
   Chord Ring:
   
   Funcionalidad: Protocolo para la organización de nodos en un anillo circular. Facilita el enrutamiento y la búsqueda eficiente de nodos responsables de ciertas claves.
   DHT (Distributed Hash Table):
   
   Funcionalidad: Mecanismo para almacenar y recuperar pares clave-valor en la red. Asegura que cada clave sea gestionada por un nodo específico.


## Configuración de parámetros

La configuración del sistema se maneja a través del archivo ```config.py```, que define varios parámetros esenciales para la operación del nodo. A continuación se detalla cada parámetro y su función:

```
# Dirección IP y puerto del nodo
SOURCE_ADDRESS = ""  # IP del nodo actual con su puerto. Ejemplo: "192.168.1.100:5001"
TARGET_ADDRESS = ""  # IP del nodo objetivo al que se conectará (en nodos de bootstrap) con su puerto.
NODE_ID = 0          # Identificador único del nodo en el anillo Chord. Debe ser un entero único.
PORT = "[::]:50051"  # Puerto en el que el nodo escuchará conexiones entrantes. El formato "[::]:50051" indica que acepta conexiones en todas las interfaces IPv6 en el puerto 50051.

```

### Parámetros a Configurar:
1. **SOURCE_ADDRESS:**

   Descripción: Especifica la dirección IP del nodo actual. Esta IP debe ser accesible para otros nodos en la red para permitir la comunicación. Si el nodo tiene una IP dinámica, asegúrate de actualizar esta dirección antes de iniciar el nodo.
   Ejemplo: "192.168.1.100"

2. **TARGET_ADDRESS:**

   Descripción: La IP del nodo al que se debe conectar inicialmente. Este parámetro se utiliza para conectarse a un nodo existente en la red y formar parte del anillo Chord. En un entorno de producción, esto podría ser un nodo de bootstrap conocido.
   Ejemplo: "192.168.1.101"

3. **NODE_ID:**

   Descripción: Identificador único del nodo en el anillo Chord. Este valor debe ser un entero único en el rango permitido para el sistema y se utiliza para organizar el nodo dentro del anillo y gestionar la asignación de claves.
   Ejemplo: 1
   
4. **PORT:**
   
   Descripción: El puerto en el que el nodo escuchará las solicitudes entrantes. El formato [::]:50051 indica que el nodo acepta conexiones en todas las interfaces de red (IPv6) en el puerto 50051. Para redes IPv4, podrías usar 0.0.0.0:50051.
   Ejemplo: "[::]:50051"

## Detalles de la organización del código por carpetas.
La estructura del proyecto está organizada de manera que cada componente tiene un propósito específico en la implementación del DHT de Chord. A continuación se detalla la organización de directorios y la función de cada archivo.

```
src/
   utils.py
   chord_dht/
       chord_client.py
       chord_services.py
       node.py
   rpc/
      chord.proto
      chord_pb2.py
      chord_pb2_grpc.py
peer.py
```

1. **utils.py** :
  - Propósito: Contiene funciones utilitarias utilizadas en toda la aplicación.
  - Función sha1_hash(key): Calcula un hash SHA-1 de la clave dada, lo convierte en un entero y devuelve el resultado módulo $2^m$. Esto se usa para hashear claves y determinar las responsabilidades de los nodos en el Chord DHT.

2. **chord_client.py** :
   - Propósito: Proporciona la funcionalidad del lado del cliente para interactuar con el DHT de Chord.
   - Función:
      - ChordClient: Clase que se conecta a un nodo del DHT a través de gRPC y ofrece métodos para encontrar sucesores, almacenar y buscar recursos.

3. **chord_services.py** :
   - Propósito: Define y gestiona los servicios gRPC que el nodo Chord ofrece.
   - Función:
      - ChordServicer: Clase que implementa los métodos del servicio Chord usando gRPC. Maneja solicitudes para encontrar sucesores, obtener predecesores, almacenar y buscar recursos, entre otros.
      - leave_network(node): Función para manejar la salida de un nodo de la red Chord, actualizando a los nodos vecinos sobre la salida.

4. **node.py** :
   - Propósito: Implementa la lógica de un nodo dentro del DHT de Chord.
   - Función:
      - Node: Clase que representa un nodo en la red Chord. Incluye métodos para encontrar sucesores, almacenar y buscar recursos, manejar la tabla de dedos, y mantener la estabilidad del nodo en la red.
      - run_background_tasks(): Método que ejecuta tareas de mantenimiento, como estabilizar y corregir la tabla de dedos del nodo en un bucle continuo.

5. **chord.proto** :
   - Propósito: Define el protocolo gRPC para la comunicación entre nodos Chord.
   - Función : Contiene las definiciones de servicios y mensajes gRPC que se utilizarán en la red Chord. Incluye definiciones para operaciones como FindSuccessor, StoreResource, LookupResource, y más.

6. **chord_pb2.proto** :
   - Función : Generado automáticamente a partir de chord.proto, contiene las clases y métodos necesarios para manipular los mensajes definidos en el archivo proto.

7. **chord_pb2_grpc.proto** :
   - Función : Generado automáticamente a partir de chord.proto, contiene las definiciones de los stubs y servicios gRPC para la comunicación entre nodos.
     

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

### Demostracion AWS
![image](https://github.com/user-attachments/assets/6a1bb50e-7e43-4469-b452-841f5d163590)
![image](https://github.com/user-attachments/assets/1a4fb743-efaf-4060-a576-8a875d34212c)
![image](https://github.com/user-attachments/assets/f6f02046-fc27-4b28-8104-b5037a96d5b8)


# 5. otra información que considere relevante para esta actividad.

### Demostración en local

![image](https://github.com/user-attachments/assets/288893f8-0a99-4f82-8511-136be67511ac)
![image](https://github.com/user-attachments/assets/f8408ee4-add1-4a08-a21b-4d3f83606efb)
![image](https://github.com/user-attachments/assets/f1cd096f-3e93-4736-9dfe-ef2415c40759)


# 6. Video sustentación del proyecto 

- **Video**: [https://www.youtube.com/watch?v=D_3f1Xvwgyw](https://www.youtube.com/watch?v=D_3f1Xvwgyw)

# referencias:

- Chord (no date) PyPI. Available at: https://pypi.org/project/chord/ (Accessed: 01 September 2024). 
- Basics tutorial (2024) gRPC. Available at: https://grpc.io/docs/languages/python/basics/ (Accessed: 01 September 2024). 



