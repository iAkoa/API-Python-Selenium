#!/bin/bash

# Création d'un environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Environnement virtuel créé."
fi

# Activation de l'environnement virtuel
source venv/bin/activate
echo "Environnement virtuel activé."

# Chemin par défaut vers le fichier JSON d'instructions
DEFAULT_INSTRUCTIONS="instructions.json"

# Vérifier si un argument (chemin du fichier JSON) a été fourni
if [ "$1" != "" ]; then
    INSTRUCTIONS_FILE=$1
else
    INSTRUCTIONS_FILE=$DEFAULT_INSTRUCTIONS
fi

pip3 install -r requirements.txt | cat > /dev/null
echo "Dépendances installées."

# Lancer l'API en utilisant le fichier JSON d'instructions spécifié ou par défaut
python3 API.py -f $INSTRUCTIONS_FILE