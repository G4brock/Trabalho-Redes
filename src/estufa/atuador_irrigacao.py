from base import atuador

def main():
    irrigacao = atuador.Atuador("ATUADOR_IRRIGACAO", "irrigacao1", "irrigacao")
    atuador.client(irrigacao)

if __name__ == "__main__":
    main()
