import sys
import os

# Ajoutez le chemin de votre application au PYTHONPATH
path = '/home/votre_username/votre_projet'
if path not in sys.path:
    sys.path.append(path)

from app import app as application  # noqa

# Configuration des variables d'environnement
os.environ['OPENAI_API_KEY'] = 'votre_clé_api_openai'
os.environ['SECRET_KEY'] = 'votre_clé_secrète'
