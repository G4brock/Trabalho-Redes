from base import atuador

def main():
    aquecedor = atuador.Atuador("ATUADOR_AQUECEDOR", "Aquecedor1", "aquecedor")
    atuador.client(aquecedor)

if __name__ == "__main__":
    main()
