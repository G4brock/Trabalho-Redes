import asyncio
import json
from os import wait
import socket
import aiohttp

def client(host="127.0.0.1", port=8000):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    # Send data
    try:
        
        data = "ATON <SP> <identificador> <LF>"#sock.recv(1000)
        data = data.split()

        timeout = aiohttp.ClientTimeout(total=1)

        with aiohttp.ClientSession(timeout=timeout) as session:
            with session.get("http://127.0.0.1:3000/server/") as response:
                    data = json.loads(response.text())
       
        print(data)

        # HELLO
        #message = "HELO temp-fake1 TEMPERATURE_SENSOR \n"
        #print("Sending %s" % message.strip("\n"))
        #sock.sendall(message.encode("utf-8"))
        #data = sock.recv(1000)
        #print("Received: %s" % data)

        #for i in range(0, 5):
        #    message = f"SEND { str(30 + i) }\n"
        #    print("Sending %s" % message.strip("\n"))
        #    sock.sendall(message.encode("utf-8"))
        #    data = sock.recv(1000)
        #    print("Received: %s" % data)

        # QUIT
        #message = "QUIT \n"
        #print("Sending %s" % message.strip("\n"))
        #sock.sendall(message.encode("utf-8"))
        #data = sock.recv(1000)
        #print("Received: %s" % data)
    except socket.error as e:
        print("Socket error: %s" % str(e))
    except Exception as e:
        print("Other exception: %s" % str(e))
    finally:
        print("Closing connection to the server")
        sock.close()

client()
