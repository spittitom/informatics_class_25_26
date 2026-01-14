# SCHRITT 1: Welches Betriebssystem?
# Wir nehmen ein fertiges Python-Image. "slim" bedeutet: nur das Nötigste, keine unnötigen Spiele oder Tools.
FROM python:3.9-slim

# SCHRITT 2: Wo arbeiten wir?
# Wir erstellen im Container einen Ordner namens /app. Ab jetzt finden alle Befehle dort statt.
WORKDIR /app

# SCHRITT 3: Die Liste der Zutaten (Requirements)
# Wir kopieren NUR die requirements.txt von deinem Laptop in den Container.
# Der Punkt am Ende bedeutet: "Kopiere es genau hierher in das aktuelle WORKDIR".
COPY requirements.txt .

# SCHRITT 4: Zutaten installieren
# Jetzt installieren wir Flask und Gunicorn im Container.
RUN pip install --no-cache-dir -r requirements.txt

# SCHRITT 5: Den Rest des Codes kopieren (Das hast du gefragt!)
# "COPY . ." bedeutet: Kopiere ALLES aus meinem aktuellen Ordner auf dem Laptop 
# (inklusive des templates-Ordners!) in den aktuellen Ordner im Container.
# Der erste Punkt steht für: "Hier bei mir auf dem Laptop".
# Der zweite Punkt steht für: "Dort im Docker-Container".
COPY . .

# SCHRITT 6: Den Ofen einschalten (Der Startbefehl)
# Wir sagen dem Container, wie er die App starten soll.
# $PORT ist eine Variable, die Render uns vorgibt.
CMD gunicorn --bind 0.0.0.0:$PORT vital_monitoring:app