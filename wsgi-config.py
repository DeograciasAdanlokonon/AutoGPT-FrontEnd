import sys
import os

# Ajoutez le chemin de votre application au PYTHONPATH
path = '/home/Casius/autogpt'
if path not in sys.path:
    sys.path.append(path)

from app import app as application  # noqa

# Configuration des variables d'environnement
os.environ['OPENAI_API_KEY'] = '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'
os.environ['SECRET_KEY'] = 'zjEJhe69566kjsgsFZkdjhdl@ejire5F£skjsd8qf^{YREJIHETYURSBHSQ654'
