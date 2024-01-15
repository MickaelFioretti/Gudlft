#!/bin/bash

# Définir le dossier de couverture
COVERAGE_DIR="coverage_data"
# Spécifier le chemin de votre package, par exemple 'app' ou '.'
COVERAGE_PATH="."

# Vérifie si un argument (nom du test) a été fourni
if [ $# -eq 0 ]
then
    echo "Aucun argument spécifié: Exécution de tous les tests avec couverture."
    pytest -q tests/ --cov=${COVERAGE_PATH} --cov-report term --cov-report html:${COVERAGE_DIR}
else
    echo "Exécution du test: $1 avec couverture."
    pytest tests/ -k "$1" --cov=${COVERAGE_PATH} --cov-report term --cov-report html:${COVERAGE_DIR}
fi