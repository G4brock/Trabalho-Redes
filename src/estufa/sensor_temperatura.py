import asyncio
from base import sensor

if __name__ == "__main__":
    try:
        print("Iniciando sensor de temperatura temp1")
        asyncio.run(sensor.main(identificador="temp1", tipo="SENSOR_TEMPERATURA"))
    except:
        pass
    finally:
        print("\nEncerrando sensor de temperatura")
