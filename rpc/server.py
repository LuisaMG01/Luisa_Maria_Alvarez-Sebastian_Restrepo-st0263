from concurrent import futures
import grpc
from . import chord_pb2 , chord_pb2_grpc
from py_chord.node2 import Node

class ChordServicer(chord_pb2_grpc.ChordServiceServicer):
    def __init__(self, node: Node):
        self.node = node

    async def Store(self, request, context):
        key = await self.node.store(request.value)
        return chord_pb2.StoreResponse(key=key.to_bytes(20, byteorder="big"))

    async def Get(self, request, context):
        print("Entre: ", request.key)
        key = int.from_bytes(request.key, byteorder="big")
        value = await self.node.get(key)
        print("Value :", value)
        value = int.to_bytes(value, byteorder="big")
        return chord_pb2.GetResponse(value=value)

    async def FindSuccessor(self, request, context):
        id_int = int.from_bytes(request.id, byteorder="big")
        successor_node = await self.node._find_successor(id_int)
        return chord_pb2.FindSuccessorResponse(
            node=chord_pb2.Node(ip=successor_node.ip, port=successor_node.port)
        )

    async def IsAlive(self, request, context):
        alive = await self.node._is_alive()
        return chord_pb2.IsAliveResponse(alive=alive)

def serve(node):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    chord_pb2_grpc.add_ChordServiceServicer_to_server(ChordServicer(node), server)
    server.add_insecure_port('[::]:50053')
    return server


