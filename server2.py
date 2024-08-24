"""from py_chord.node2 import Node, RemoteNode
from rpc.server import serve
import asyncio
from py_chord import join_network

async def main():
    # Crear el segundo nodo
    node = Node(ip="127.0.0.1", port=50053)
    node._alive = True  # Simulamos que el nodo está vivo
        
    server = serve(node)
    await server.start()
    
    print("Servidor gRPC Nodo 2 corriendo en 127.0.0.1:50053")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(main())
"""

from py_chord.node2 import Node, RemoteNode
from rpc.server import serve
import asyncio
from py_chord import join_network

async def main():
    
    # Crear el segundo nodo
    node2 = Node(ip="127.0.0.1", port=50053)
    node2._alive = True  # Simulamos que el nodo está vivo

    # Iniciar el servidor para el segundo nodo
    server = serve(node2)
    await server.start()
    print("Servidor gRPC Nodo 2 corriendo en 127.0.0.1:50053")


    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(main())

