# client.py
import asyncio
import grpc
from rpc.chord_pb2 import StoreRequest, GetRequest
from rpc.chord_pb2_grpc import ChordServiceStub

async def main():
    # Conectar al Nodo 1 (gRPC en 127.0.0.1:50051)
    async with grpc.aio.insecure_channel('127.0.0.1:50051') as channel:
        stub = ChordServiceStub(channel)

        # Almacenar un archivo en la red
        file_data = b"Este es un archivo de prueba."
        print("Almacenando archivo en Nodo 1...")
        response = await stub.Store(StoreRequest(value=file_data))
        key_bytes = response.key  # Aquí obtenemos directamente los bytes
        #key = int.from_bytes(key_bytes, byteorder="big")  # Convertimos a int para mostrar la clave
        print(f"Archivo almacenado con la clave: {key_bytes}")
      
        # Conectar al Nodo 2 (gRPC en 127.0.0.1:50052) para recuperar el archivo
        async with grpc.aio.insecure_channel('127.0.0.1:50053') as channel2:
            stub2 = ChordServiceStub(channel2)
            print("Recuperando archivo desde Nodo 2...")
            get_response = await stub2.Get(GetRequest(key=key_bytes))  # Aquí pasamos los bytes tal cual
            retrieved_file = get_response.value
            print(f"Archivo recuperado: {retrieved_file}")

if __name__ == '__main__':
    asyncio.run(main())

