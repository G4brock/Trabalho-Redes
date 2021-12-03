import json
import socket
import requests

nome_limites = ["MAX_TEMP", "MIN_TEMP", "MAX_UMID", "MIN_UMID", "MAX_CO2", "MIN_CO2"]
tipo_atuadores = ["irrigacao", "aquecedor", "injetorco2", "resfriador"]


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
        print("\n\nO que deseja fazer? (conf, ler, oper, sair)")
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

        if resposta == "oper":
            print("\tTipos: aquecedor, resfriador, injetorco2 ou irrigacao.")
            print("\tEstado: true ou false\n")
            
            atuador = input("Qual atuador você deseja operar? ")
            estado = input("Qual o estado que você deseja colocar esse atuador?")
            tipo = input("Qual o tipo de atuador? ")

            if (estado.lower() == "true" or "false") and (tipo in tipo_atuadores):
                response = requests.post(f"http://127.0.0.1:3000/{atuador}/{estado}/{tipo}")
                print(response)
            else:
                print(f"valor inválido")

        if resposta == "sair":
            raise Exception


if __name__ == "__main__":
    try:
        cliente()
    except:
        print("\n")
        exit(1)
