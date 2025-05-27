# Wybieramy obraz bazowy z Pythona
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki projektu do kontenera
COPY . .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Otwieramy port aplikacji
EXPOSE 5000

# Komenda do uruchomienia aplikacji
CMD ["python", "run.py"]
