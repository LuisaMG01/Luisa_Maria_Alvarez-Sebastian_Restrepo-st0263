# Arquitectura P2P y Comunicación entre Procesos mediante API REST, RPC y MOM

### Descripción

Este proyecto implementa un sistema de compartición de archivos distribuido y descentralizado basado en una red P2P estructurada utilizando Chord/DHT, o una alternativa similar. Cada nodo (peer) contiene microservicios para manejar la comunicación, el almacenamiento de archivos y el mantenimiento de la red P2P. El sistema soporta concurrencia y utiliza middleware para comunicación RPC con gRPC.


### Requisitos

- Python 3.x
- Flask
- gRPC

## Arquitectura


### Red P2P

El sistema está basado en una red P2P estructurada utilizando el protocolo Chord o una alternativa similar. Los nodos en la red se comunican entre sí para mantener la red y localizar recursos.

### Componentes
- Servidor: Microservicios en el nodo que permiten la carga, descarga y listado de archivos. Estos microservicios deben soportar concurrencia para permitir múltiples conexiones simultáneas.
- Cliente: Módulo cliente que interactúa con los nodos para cargar o descargar archivos.
