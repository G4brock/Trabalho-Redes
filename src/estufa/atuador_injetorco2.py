from base import atuador

def main():
    injetorco2 = atuador.Atuador("ATUADOR_INJETORCO2", "injetor1", "injetorco2")
    atuador.client(injetorco2)

if __name__ == "__main__":
    main()
