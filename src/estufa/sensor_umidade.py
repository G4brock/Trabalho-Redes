import asyncio
from base import sensor

if __name__ == "__main__":
    try:
        print("Iniciando sensor de umidade umi1")
        asyncio.run(sensor.main(identificador="umi1", tipo="SENSOR_UMIDADE"))
    except:
        pass
    finally:
        print("\nEncerrando sensor de umidade")
