import json
import threading
import time
from http import server
from collections import namedtuple

TEMPERATURA = 30
UMIDADE = 50
CO2 = 10
ATUADORES = []


class ThreadSimulador(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global TEMPERATURA
        global UMIDADE
        global CO2
        global ATUADORES
        
        while True:
            correcao()
            for atuador in ATUADORES:
                if atuador["status"] == True:
                    if atuador["tipo"] == "aquecedor":
                        TEMPERATURA = TEMPERATURA + 5
                    if atuador["tipo"] == "resfriador":
                        TEMPERATURA = TEMPERATURA - 5
                    if atuador["tipo"] == "irrigacao":
                        UMIDADE = UMIDADE + 3
                    if atuador["tipo"] == "injetorco2":
                        CO2 = CO2 + 10
            time.sleep(1)


class ServidorWeb(server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        valores = {"temperatura": TEMPERATURA, "umidade": UMIDADE, "co2": CO2}
        self.wfile.write(json.dumps(valores).encode("utf-8"))

    def do_POST(self) -> None:
        global ATUADORES
        valores = self.path.strip().split("/")
        novo = True
        for atuador in ATUADORES:
            if atuador["identificador"] == valores[1]:
                atuador["status"] = True if valores[2].lower() == "true" else False
                novo = False

        if novo:
            ATUADORES.append(
                {
                    "identificador": valores[1],
                    "status": True if valores[2].lower() == "true" else False,
                    "tipo": valores[3],
                }
            )

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        valores = {
            "identificador": valores[1],
            "status": True if valores[2].lower() == "true" else False,
            "tipo": valores[3],
        }
        self.wfile.write(json.dumps(valores).encode("utf-8"))


class ThreadWeb(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        httpd = server.HTTPServer(("127.0.0.1", 3000), ServidorWeb)
        httpd.serve_forever()

def correcao():
    global TEMPERATURA
    global CO2
    global UMIDADE

    TEMPERATURA += 0.1
    CO2 -= 0.05
    UMIDADE -= 0.1


if __name__ == "__main__":
    servidor = ThreadWeb("servidor-web")
    simulador = ThreadSimulador("simulador")

    servidor.start()
    simulador.start()

    servidor.join()
    simulador.join()
