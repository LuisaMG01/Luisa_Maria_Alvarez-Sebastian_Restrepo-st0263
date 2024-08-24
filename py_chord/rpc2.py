import grpc
from rpc import chord_pb2, chord_pb2_grpc
from .abc import INode

async def store(dst: INode, value: bytes) -> int:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.Store(chord_pb2.StoreRequest(value=value))
        return response.key

async def get(dst: INode, key: int) -> bytes:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.Get(chord_pb2.GetRequest(key=key))
        return response.value

async def is_alive(dst: INode) -> bool:
    try:
        async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
            stub = chord_pb2_grpc.ChordServiceStub(channel)
            response = await stub.IsAlive(chord_pb2.IsAliveRequest())
            return response.alive
    except grpc.RpcError:
        return False

async def closest_preceding_finger(dst: INode, id: int) -> INode:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.ClosestPrecedingFinger(chord_pb2.FindSuccessorRequest(id=id))
        return INode(response.node.ip, response.node.port)

async def find_successor(dst: INode, id: int) -> INode:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.FindSuccessor(chord_pb2.FindSuccessorRequest(id=id))
        return INode(response.node.ip, response.node.port)

async def notify(dst: INode, node: INode) -> None:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        await stub.Notify(chord_pb2.NotifyRequest(node=chord_pb2.Node(ip=node.ip, port=node.port)))

async def update_finger_table(dst: INode, node: INode, index: int) -> None:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        await stub.UpdateFingerTable(chord_pb2.UpdateFingerTableRequest(node=chord_pb2.Node(ip=node.ip, port=node.port), index=index))

async def get_successor(dst: INode) -> INode:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.GetSuccessor(chord_pb2.GetSuccessorRequest())
        return INode(response.node.ip, response.node.port)

async def set_successor(dst: INode, node: INode) -> None:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        await stub.SetSuccessor(chord_pb2.SetSuccessorRequest(node=chord_pb2.Node(ip=node.ip, port=node.port)))

async def get_predecessor(dst: INode) -> INode:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        response = await stub.GetPredecessor(chord_pb2.GetPredecessorRequest())
        return INode(response.node.ip, response.node.port)

async def set_predecessor(dst: INode, node: INode) -> None:
    async with grpc.aio.insecure_channel(f'{dst.ip}:{dst.port}') as channel:
        stub = chord_pb2_grpc.ChordServiceStub(channel)
        await stub.SetPredecessor(chord_pb2.SetPredecessorRequest(node=chord_pb2.Node(ip=node.ip, port=node.port)))
