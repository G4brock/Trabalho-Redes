import asyncio
import json
from os import wait
import socket
import requests

class Atuador:
    def __init__(self, tipo, identificador, tipo2):
        self.tipo = tipo
        self.identificador = identificador
        self.tipo2 = tipo2
        
def client(atuador, host="127.0.0.1", port=8000):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    # Send data
    try:
        sock.send(f"HELO { atuador.identificador } {atuador.tipo}\n".encode("utf-8"))
        while True:
            data = sock.recv(1000)
            print(data.decode("utf-8"), "A")
            data = data.decode().split()
            print("\t" + data[1])
            if data[1] == atuador.identificador:
                if data[0] == "ATON":
                    requests.post('http://127.0.0.1:3000/' + atuador.identificador + '/true/' + atuador.tipo2)
                if data[0] == "ATOF":
                    requests.post('http://127.0.0.1:3000/' + atuador.identificador + '/false/' + atuador.tipo2)
                
            sock.send("200 OK".encode("utf-8"))
        
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()
