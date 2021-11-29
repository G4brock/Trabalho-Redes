import asyncio
import json
from asyncio import transports
from collections import namedtuple
from typing import final, Union
from exceptions import IdentificadorEmUso

Conections = namedtuple("Conection", ["id", "type", "transport"])

leituras = {}
conexoes = []


class GerenciadorProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        self.identificador = None
        super().__init__()

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        return super().connection_made(transport)

    def data_received(self, data: bytes) -> None:
        message = data.decode().strip()
        print(f"Mensagem recebida: { message }; De: { self.identificador }")
        message = message.split(" ")

        command = message[0]
        if command == "HELO":
            try:
                identificador = message[1]
                for con in conexoes:
                    if con.id == identificador:
                        raise IdentificadorEmUso

                self.identificador = identificador
                self.conexao = Conections(
                    self.identificador, message[2], self.transport
                )
                conexoes.append(self.conexao)
            except IdentificadorEmUso:
                self.transport.write("410 Identificador em uso.".encode("utf-8"))
                self.transport.close()
            except:
                self.transport.write("500 Ocorreu um erro\n".encode("utf-8"))
            else:
                self.transport.write(f"220 gerenciador Pronto\n".encode("utf-8"))

        if self.identificador == None:
            self.transport.write("500 Ocorreu um erro\n".encode("utf-8"))
            return

        if command == "SEND":
            try:
                leituras[self.identificador] = int(message[1])
            except:
                self.transport.write("500 Ocorreu um erro\n".encode("utf-8"))
            else:
                self.transport.write("200 Ok\n".encode("utf-8"))

        if command == "READ":
            try:
                _identificador = message[1]
                if _identificador == "ALL":
                    valor = json.dumps(leituras, separators=(",", ""))
                else:
                    valor = json.dumps({_identificador: leituras[_identificador]})
                self.transport.write(f"230 { valor }\n".encode("utf-8"))
            except:
                self.transport.write("500 Ocorreu um erro\n".encode("utf-8"))

        if command == "ATON":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    c.transport.write(f"ATON { _identificador }\n".encode("utf-8"))

        if command == "ATOF":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    c.transport.write(f"ATOF { _identificador }\n".encode("utf-8"))

        if command == "QUIT":
            self.transport.write("200 Ok\n".encode("utf-8"))
            self.transport.close()

        return super().data_received(data)

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        if self.identificador:
            for con in conexoes:
                if con.id == self.identificador:
                    conexoes.remove(con)

            if self.identificador in leituras.keys():
                leituras.pop(self.identificador)

        return super().connection_lost(exc)


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
