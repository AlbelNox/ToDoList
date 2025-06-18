#Dockerfile

#Basisimage für Python-Anwendung herunterladen
FROM python:3.8-alpine

# Notwendige Biblitheken installieren
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Arbeitsverzeichnis im Container wechseln
WORKDIR /app

# Kopiere lokale Datei in das Container-Image
COPY src/server.py /app

# Konfiguriere den Befehl, der im Container ausgeführt werden soll
# (Anwendung Python + Skriptname als Parameter)
ENTRYPOINT [ "python" ]
CMD ["server.py"]