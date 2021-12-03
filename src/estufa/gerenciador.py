import asyncio
import json
from asyncio.transports import BaseTransport
from collections import namedtuple
from dataclasses import dataclass
from typing import final, Union, List
from exceptions import IdentificadorEmUso

Conections = namedtuple("Conection", ["id", "type", "transport"])


@dataclass
class Atuador:
    id: str
    type: str
    conn: BaseTransport
    status: bool


atuadores: List[Atuador] = []
leituras = {}
conexoes = []
limites = {
    "MAX_TEMP": 40,
    "MIN_TEMP": 20,
    "MAX_UMID": 50,
    "MIN_UMID": 30,
    "MAX_CO2": 50,
    "MIN_CO2": 10,
}


def enviar_mensagem(msg: str, transport: BaseTransport, id: str) -> None:

    print(f'Enviando > Para: {id}\tMensagem: "{msg.strip()}";')
    transport.write(msg.encode("utf-8"))


class GerenciadorProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        self.identificador = None
        self.tipo = None
        super().__init__()

    def connection_made(self, transport: BaseTransport) -> None:
        self.transport = transport
        return super().connection_made(transport)

    def responder(self, message: str):
        enviar_mensagem(message, self.transport, self.identificador)

    def data_received(self, data: bytes) -> None:
        message = data.decode().strip()
        print(f'Recebida < De :{ self.identificador }\tMensagem: "{ message }";')
        message = message.split(" ")

        command = message[0]
        if command == "HELO":
            try:
                identificador = message[1]
                for con in conexoes:
                    if con.id == identificador:
                        raise IdentificadorEmUso

                self.identificador = identificador
                self.tipo = message[2].lower().split("_")[1]
                self.conexao = Conections(
                    self.identificador, message[2], self.transport
                )

                if "ATUADOR" in message[2]:
                    atuadores.append(
                        Atuador(
                            id=self.identificador,
                            type=message[2],
                            conn=self.transport,
                            status=False,
                        )
                    )

                conexoes.append(self.conexao)
            except IdentificadorEmUso:
                self.responder("410 Identificador em uso.\n")
                self.transport.close()
            except:
                self.responder("500 Ocorreu um erro\n")
            else:
                self.responder("220 gerenciador Pronto\n")

        if self.identificador == None:
            self.responder("500 Ocorreu um erro\n")
            return

        if command == "ATPA":
            try:
                param = message[1]
                valor = float(message[2])

                if param in limites.keys():
                    limites[param] = valor
                    self.responder("200 Ok\n")
                else:
                    raise Exception
            except:
                self.responder("500 Ocorreu um erro\n")

        if command == "SEND":
            try:
                leituras[self.identificador] = float(message[1])
            except:
                self.responder("500 Ocorreu um erro\n")
            else:
                self.responder("200 Ok\n")

        if command == "READ":
            try:
                _identificador = message[1]
                valor = {}
                if _identificador == "ALL":

                    valor = json.dumps(
                        {"leituras": leituras, "limites": limites},
                        separators=(",", ":"),
                    )
                else:
                    valor = json.dumps({_identificador: leituras[_identificador]})
                self.responder(f"230 { valor }\n")
            except:
                self.responder("500 Ocorreu um erro\n")

        if command == "ATON":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    enviar_mensagem(f"ATON { _identificador }\n", c.trasport, c.id)

        if command == "ATOF":
            _identificador = message[1]
            for c in conexoes:
                if c.id == _identificador:
                    enviar_mensagem(f"ATOF { _identificador }\n", c.trasport, c.id)

        if command == "QUIT":
            self.responder("200 Ok\n")
            self.transport.close()

        return super().data_received(data)

    def connection_lost(self, exc: Union[Exception, None]) -> None:
        if self.identificador:
            for con in conexoes:
                if con.id == self.identificador:
                    conexoes.remove(con)

            if self.identificador in leituras.keys():
                leituras.pop(self.identificador)

            for at in atuadores:
                if at.id == self.identificador:
                    atuadores.remove(at)

        return super().connection_lost(exc)


async def controlador():
    while True:
        ligar = []
        desligar = []
        for conn in conexoes:
            if conn.type == "SENSOR_TEMPERATURA":
                if leituras[conn.id] < limites["MIN_TEMP"]:
                    ligar.append("ATUADOR_AQUECEDOR")
                if leituras[conn.id] > limites["MAX_TEMP"]:
                    ligar.append("ATUADOR_RESFRIADOR")
                if leituras[conn.id] > limites["MIN_TEMP"]:
                    desligar.append("ATUADOR_AQUECEDOR")
                if leituras[conn.id] < limites["MAX_TEMP"]:
                    desligar.append("ATUADOR_RESFRIADOR")
            if conn.type == "SENSOR_UMIDADE":
                if leituras[conn.id] < limites["MIN_UMID"]:
                    ligar.append("ATUADOR_IRRIGACAO")
                if leituras[conn.id] > limites["MAX_UMID"]:
                    desligar.append("ATUADOR_IRRIGACAO")
            if conn.type == "SENSOR_CO2":
                if leituras[conn.id] > limites["MAX_CO2"]:
                    ligar.append("ATUADOR_INJETORCO2")
                if leituras[conn.id] < limites["MIN_CO2"]:
                    desligar.append("ATUADOR_INJETORCO2")

        for at in atuadores:
            if at.type in ligar and at.status == False:
                enviar_mensagem(f"ATON { at.id }\n", at.conn, at.id)
                at.status = True
            if at.type in desligar and at.status == True:
                enviar_mensagem(f"ATOF { at.id }\n", at.conn, at.id)
                at.status = False
        await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(lambda: GerenciadorProtocol(), "127.0.0.1", 8000)

    asyncio.run(await controlador())
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
