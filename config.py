import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-difficile-a-deviner'
    
    # Configuration des uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Configuration OpenAI (AutoGPT)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    # OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Configuration de la base de données (si nécessaire)
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
