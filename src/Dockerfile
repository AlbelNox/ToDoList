#-doockerfile

#Basisimage für Python-Anwendung herunterladen
FROM python:3.12-alpine

# Arbeitsverzeichnis im Container wechseln
WORKDIR /app

# Notwendige Biblitheken installieren
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere lokale Datei in das Container-Image
COPY server.py /app

# Konfiguriere den Befehl, der im Container ausgeführt werden soll
# (Anwendung Python + Skriptname als Parameter)
ENTRYPOINT [ "python" ]
CMD ["server.py"]

