import asyncio, logging
from hashlib import sha1
from typing import Any

from . import rpc2
from .abc import INode, INodeServer
from .errors import InvalidRPC, NodeLeaveError
from .network import is_between_ids, ChordNetwork, CHORD_PORT, MAINTENANCE_FREQUENCY

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def node_leave_corrector(func, retry_time=MAINTENANCE_FREQUENCY, max_retries=2):
    async def wrapper(self, *args, retries=0, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except NodeLeaveError:
            if retries >= max_retries:
                raise NodeLeaveError(f"Exceeded maximum retries amount: {max_retries}")
            self.network.remove_left_node(self)
            await asyncio.sleep(retry_time)
            await wrapper(self, *args, retries=retries + 1, **kwargs)

    return wrapper

class Node(INode, INodeServer):
    def __init__(self, ip: str, port: int = CHORD_PORT):
        super().__init__(ip, port)
        self.network = ChordNetwork(self)
        self.hash_table = {}
        self._predecessor = None
        self._alive = False
    
    def print_finger_table(self):
        print(f"Finger Table for Node {self.id} ({self.ip}:{self.port}):")
        for i, finger in enumerate(self.network.finger_table):
            if finger.node:
                print(f"  Finger {i}: start={finger.start}, end={finger.end}, points to Node {finger.node.id} ({finger.node.ip}:{finger.node.port})")
            else:
                print(f"  Finger {i}: start={finger.start}, end={finger.end}, points to None")

    async def store(self, value: bytes) -> int:
        if not isinstance(value, bytes):
            raise InvalidRPC()
        key = self._get_key_from_value(value)
        print("La key es : " , key)
        successor = await self._find_successor(key)
        if successor == self:
            logger.debug(f"({self.id}) - Stored value in local node: {key}")
            self.hash_table[key] = value
        else:
            await successor.store(value)
        return key

    async def get(self, key: int) -> Any:
        successor = await self._find_successor(key)
        if successor == self:
            return self.hash_table.get(key)
        else:
            return await successor.get(key)

    async def leave(self) -> None:
        self._alive = False

    async def _is_alive(self) -> bool:
        return self._alive

    async def _closest_preceding_finger(self, id: int) -> INode:
        for finger in reversed(self.network.finger_table):
            if finger.node and is_between_ids(finger.node.id, self.id, id):
                return finger.node
        return self

    @node_leave_corrector
    async def _find_successor(self, id: int) -> INode:
        predecessor = await self.network._find_predecessor(id)
        successor = await predecessor._get_successor()
        return successor

    async def _notify(self, node: INode) -> None:
        if not self._predecessor or is_between_ids(node.id, self._predecessor.id, self.id):
            self._predecessor = node

    async def _update_finger_table(self, node: INode, index: int) -> None:
        finger = self.network.finger_table[index]
        if not finger.node or is_between_ids(node.id, finger.start, finger.node.id, first_equality=True):
            finger.node = node
            if self._predecessor and self._predecessor != self:
                await self._predecessor._update_finger_table(node, index)

    async def _get_successor(self) -> INode:
        for finger in self.network.finger_table:
            if finger.node:
                return finger.node
        return self

    async def _set_successor(self, node: INode) -> None:
        self.network.finger_table[0].node = node

    async def _get_predecessor(self) -> INode:
        if self._predecessor:
            return self._predecessor
        for finger in reversed(self.network.finger_table):
            if finger.node:
                return finger.node
        return self

    async def _set_predecessor(self, node: INode) -> None:
        self._predecessor = node

    def _get_key_from_value(self, value):
        hash = sha1()
        hash.update(value)
        return int.from_bytes(hash.digest(), "big")
    
    async def _start_server(self):
        """Método abstracto de INodeServer. Implementación vacía para cumplir con la clase abstracta."""
        pass

    async def _stop_server(self):
        """Método abstracto de INodeServer. Implementación vacía para cumplir con la clase abstracta."""
        pass

class RemoteNode(INode):
    def __init__(self, ip: str, port: int = CHORD_PORT):
        super().__init__(ip, port)

    async def store(self, value: bytes) -> None:
        await rpc2.store(self, value)

    async def get(self, key: int) -> Any:
        return await rpc2.get(self, key)

    async def _is_alive(self) -> bool:
        return await rpc2.is_alive(self)

    async def _closest_preceding_finger(self, id: int) -> INode:
        return await rpc2.closest_preceding_finger(self, id)

    async def _find_successor(self, id: int) -> INode:
        return await rpc2.find_successor(self, id)

    async def _notify(self, node: INode) -> None:
        return await rpc2.notify(self, node)

    async def _update_finger_table(self, node: INode, index: int) -> None:
        return await rpc2.update_finger_table(self, node, index)

    async def _get_successor(self) -> INode:
        return await rpc2.get_successor(self)

    async def _set_successor(self, node: INode) -> None:
        return await rpc2.set_successor(self, node)

    async def _get_predecessor(self) -> INode:
        return await rpc2.get_predecessor(self)

    async def _set_predecessor(self, node: INode) -> None:
        return await rpc2.set_predecessor(self, node)
