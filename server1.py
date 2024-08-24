from py_chord.node2 import Node
from rpc.server import serve
import asyncio

async def main():
    node = Node(ip="127.0.0.1", port=50051)
    node._alive = True  # Simulamos que el nodo está vivo
    server = serve(node)
    await server.start()
    print("Servidor gRPC Nodo 1 corriendo en 127.0.0.1:50051")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(main())