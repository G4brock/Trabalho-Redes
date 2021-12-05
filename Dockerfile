FROM python:3.8
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./
COPY run.sh ./
COPY cliente.sh ./

RUN ["chmod", "+x", "/app/run.sh"]
RUN ["chmod", "+x", "/app/cliente.sh"]

EXPOSE 8000/tcp
EXPOSE 3000/tcp

CMD ["/app/run.sh"]