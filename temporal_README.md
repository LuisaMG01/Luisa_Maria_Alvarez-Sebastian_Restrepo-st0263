# ST0263 Tópicos en telemática

## Estudiantes:
- Luisa María Álvarez García, lmalvarez8@eafit.edu.co
- Sebastián Restrepo Ortiz, srestrep74@eafit.edu.co

## Profesor: 
- Edwin Nelson Montoya Múnera, emontoya@eafit.edu.co

## Descripción

Este proyecto implementa un sistema de compartición de archivos distribuido y descentralizado basado en una red P2P estructurada utilizando Chord/DHT, o una alternativa similar. Cada nodo (peer) contiene microservicios para manejar la comunicación, el almacenamiento de archivos y el mantenimiento de la red P2P. El sistema soporta concurrencia y utiliza middleware para comunicación RPC con gRPC.

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

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

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

Para ejecutar un nodo Chord:

```
python server.py <node_id> <server_address> <join_address>
```

Donde:
- `<node_id>`: Es un número entero que identifica al nodo.
- `<server_address>`: Es la dirección IP y puerto donde el nodo escuchará (ej. "localhost:50051").
- `<join_address>`: Es la dirección de un nodo existente para unirse a la red. Use "none" para iniciar una nueva red.

Ejemplos:

1. Iniciar el primer nodo (nueva red):
   ```
   python server.py 0 localhost:50051 none
   ```
2. Unir un segundo nodo a la red existente:
  ```
   python server.py 1 localhost:50052 localhost:50051
  ```

### Ejecución con Docker

En caso de preferir usar Docker:

1. Construye la imagen:
   ```
  docker build -t chord-node .
  ```

2. Ejecuta un contenedor:
  ```
  docker run -p 50051:50051 chord-node python server.py 0 0.0.0.0:50051 none
  ```

Para nodos adicionales, ajusta el puerto mapeado y los parámetros según sea necesario.

### Interacción con el Nodo

Una vez que el nodo esté en ejecución, seguirá las instrucciones en la consola para interactuar con él. Puedes almacenar recursos, buscar recursos, imprimir la tabla de dedos o salir del programa.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## detalles del desarrollo.
## detalles técnicos
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto




