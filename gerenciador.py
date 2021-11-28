import asyncio
import json
from asyncio import transports
from collections import namedtuple
from typing import final

Conections = namedtuple("Conection", ["id", "type", "transport"])

leituras = {}
conexoes = []


class GerenciadorProtocol(asyncio.Protocol):
    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        return super().connection_made(transport)

    def data_received(self, data: bytes) -> None:
        message = data.decode().strip().split(" ")
        print(f"Mensagem recebida: {{ message }}")

        command = message[0]
        if command == "HELO":
            try:
                self.identificador = message[1]
                conexoes.append(
                    Conections(self.identificador, message[2], self.transport)
                )
            except:
                self.transport.write("500 Ocorreu um erro\n")
            else:
                self.transport.write(f"220 {{ values['name'] }} Pronto\n")

        if command == "SEND":
            try:
                leituras[self.identificador] = int(message[1])
            except:
                self.transport.write("500 Ocorreu um erro\n")
            else:
                self.transport.write("200 Ok\n")

        if command == "READ":
            try:
                _identificador = message[1]
                if _identificador == "ALL":
                    valor = json.dumps(leituras, separators=(",", ""))
                else:
                    valor = json.dumps({_identificador: leituras[_identificador]})
                self.transport.write(f"xxx {{ valor }}\n")
            except:
                self.transport.write("500 Ocorreu um erro\n")
            else:
                self.transport.write("200 Ok\n")

        if command == "ATON":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    c.transport.write(f"ATON {{ _identificador }}\n")

        if command == "ATOF":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    c.transport.write(f"ATOF {{ _identificador }}\n")

        if command == "QUIT":
            self.transport.write("200 Ok\n")
            self.transport.close()

        return super().data_received(data)


async def main():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(lambda: GerenciadorProtocol(), "127.0.0.1", 8000)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        print("Iniciando o servidor.")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEncerrando o servidor...")
        for c in conexoes:
            c.transport.close()
    finally:
        print("Pronto.")
