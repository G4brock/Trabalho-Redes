import asyncio
import json
from os import wait
import socket
import aiohttp

VALOR = 30


async def sensor(identificador: str, tipo: str):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8000)

    writer.write(f"HELO { identificador } {tipo} \n".encode("utf-8"))
    await writer.drain()

    response = await reader.readline()
    if response.decode().split(" ")[0] != "220":
        raise Exception

    while True:
        try:
            writer.write(f"SEND { VALOR }\n".encode())
            await writer.drain()

            response = await reader.readline()
            if response.decode().split(" ")[0] != "200":
                raise Exception
        except:
            pass
        finally:
            await asyncio.sleep(1)


async def get_data(medida: str):
    global VALOR
    timeout = aiohttp.ClientTimeout(total=1)
    while True:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get("http://127.0.0.1:3000/server/") as response:
                    data = json.loads(await response.text())
                    VALOR = data[medida]
        except:
            pass
        finally:
            await asyncio.sleep(1)


async def main(identificador: str, tipo: str):
    await asyncio.wait(
        [
            asyncio.create_task(get_data(tipo.lower().split("_")[1])),
            asyncio.create_task(sensor(identificador, tipo)),
        ]
    )


if __name__ == "__main__":
    try:
        asyncio.run(main("fake1", "SENSOR_TEMPERATURA"))
    except:
        print("\nEncerrando o servidor.")
