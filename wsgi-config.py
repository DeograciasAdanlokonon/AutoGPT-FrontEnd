import sys
import os

# Ajoutez le chemin de votre application au PYTHONPATH
path = '/home/Casius/autogpt'
if path not in sys.path:
    sys.path.append(path)

from app import app as application  # noqa

# Configuration des variables d'environnement
os.environ['OPENAI_API_KEY'] = 'your_key'
os.environ['SECRET_KEY'] = 'your_secret_key'
