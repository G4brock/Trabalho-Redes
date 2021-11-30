from base import atuador

def main():
    resfriador = atuador.Atuador("ATUADOR_RESFRIADOR", "resfriador1", "resfriador")
    atuador.client(resfriador)

if __name__ == "__main__":
    main()
