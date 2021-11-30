#!/bin/sh
PYTHONUNBUFFERED=1

exec python3 estufa/gerenciador.py &
exec python3 sim-py/simulador.py &
exec python3 estufa/sensor_co2.py &
exec python3 estufa/sensor_temperatura.py &
exec python3 estufa/sensor_umidade.py &
exec python3 estufa/atuador_aquecedor.py &
exec python3 estufa/atuador_injetorco2.py &
exec python3 estufa/atuador_irrigacao.py &
exec python3 estufa/atuador_resfriador.py