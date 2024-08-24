import asyncio
from py_chord import join_network

async def main():
    host = "127.0.0.1"
    port = 8888
    bootstrap_node = ("127.0.0.1", 7777)

    network = await join_network(host, port, bootstrap_node)
    
    # Espera unos segundos para asegurar que el Nodo 1 haya almacenado el archivo
    await asyncio.sleep(5)


    file_key = input("Ingrese la clave del archivo para recuperar: ")  # Clave proporcionada por el nodo 1
    retrieved_file = await network.get(int(file_key))

    if retrieved_file:
        print(f"Node 2 successfully retrieved the file: {retrieved_file.decode()}")
    else:
        print("File not found or retrieval failed")

    # Dejar la red cuando termine
    await network.leave()

if __name__ == "__main__":
    asyncio.run(main())
