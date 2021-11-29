import asyncio
from base import sensor

if __name__ == "__main__":
    try:
        print("Iniciando sensor de CO2 co1")
        asyncio.run(sensor.main(identificador="co1", tipo="SENSOR_CO2"))
    except:
        pass
    finally:
        print("\nEncerrando sensor de CO2")
