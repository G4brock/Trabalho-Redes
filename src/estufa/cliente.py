import json
import socket

nome_limites = ["MAX_TEMP", "MIN_TEMP", "MAX_UMID", "MIN_UMID", "MAX_CO2", "MIN_CO2"]


def cliente():
    # conectar
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 8000))
    sock.send(f"HELO cliente CLIENTE_CLIENTE\n".encode("utf-8"))
    response = sock.recv(1000).decode("utf-8")

    if response.split(" ")[0] != "220":
        print("Erro ao conectar ao gerenciador.")
        exit(0)

    print("Bem vindo a estufa inteligente.")

    # menu
    while True:
        print("\n\nO que deseja fazer? (conf, ler, sair)")
        resposta = input()

        # configuar
        if resposta == "conf":
            print("Qual valor quer configurar?")
            print("(MAX_TEMP, MIN_TEMP, MAX_UMID, MIN_UMID, MAX_CO2, MIN_CO2)".lower())
            resposta = input().upper()
            if resposta in nome_limites:
                valor = input("\nQual o valor?\n")
                sock.send(f"ATPA {resposta} {float(valor)} \n".encode("utf-8"))
                response = sock.recv(1000).decode("utf-8").split(" ")
                continue

        # ler
        if resposta == "ler":
            sock.send(f"READ ALL \n".encode("utf-8"))
            response = sock.recv(1000).decode("utf-8").split(" ")
            if response[0]:
                r = json.loads(response[1])
                print("Leituras:\t", r["leituras"])
                print("Limites:\t", r["limites"])

        if resposta == "sair":
            raise Exception


if __name__ == "__main__":
    try:
        cliente()
    except:
        print("\n")
        exit(1)
