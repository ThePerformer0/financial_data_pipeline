FROM python:3.9-slim-buster

# Définition du répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie des fichiers de dépendances pour les installer
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt