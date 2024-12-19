# Projet Interface Upload & Chat AutoGPT

## Structure du projet
```
votre_projet/
├── README.md
├── app.py              # Application Flask principale
├── config.py           # Configuration de l'application
├── flask_app.py        # Configuration WSGI PythonAnywhere
├── requirements.txt    # Dépendances Python
├── static/
│   └── js/
│       └── app.js     # Interface React
├── templates/
│   └── index.html     # Template HTML principal
└── uploads/           # Dossier pour les fichiers uploadés
```

## Installation

1. **Prérequis**
   - Compte PythonAnywhere
   - Python 3.8+
   - pip (gestionnaire de paquets Python)
   - Clé API OpenAI

2. **Installation locale pour tests**
   ```bash
   # Cloner le projet
   git clone [URL_DU_REPO]
   cd votre_projet

   # Créer un environnement virtuel
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate

   # Installer les dépendances
   pip install -r requirements.txt
   ```

3. **Configuration locale**
   - Copier `.env.example` vers `.env`
   - Remplir les variables d'environnement :
     ```
     OPENAI_API_KEY=votre_clé_api
     SECRET_KEY=votre_clé_secrète
     ```

## Déploiement sur PythonAnywhere

1. **Création de l'application**
   - Se connecter à PythonAnywhere
   - Aller dans la section "Web"
   - Cliquer sur "Add a new web app"
   - Choisir "Flask" comme framework
   - Sélectionner Python 3.8 ou supérieur

2. **Configuration du projet**
   - Dans l'onglet "Files"
     1. Créer un nouveau dossier : `/home/votre_username/votre_projet`
     2. Uploader tous les fichiers du projet dans ce dossier
     3. Vérifier que la structure des dossiers est correcte

   - Dans l'onglet "Web"
     1. Configurer le "Source code" : `/home/votre_username/votre_projet`
     2. Configurer le "Working directory" : `/home/votre_username/votre_projet`
     3. Pointer le "WSGI file" vers `flask_app.py`

3. **Configuration des variables d'environnement**
   - Dans l'onglet "Web"
   - Section "Environment variables"
   - Ajouter :
     ```
     OPENAI_API_KEY=votre_clé_api
     SECRET_KEY=votre_clé_secrète
     ```

4. **Installation des dépendances**
   - Ouvrir une console PythonAnywhere
   - Naviguer vers le dossier du projet
   - Exécuter :
     ```bash
     pip3 install --user -r requirements.txt
     ```

5. **Configuration des permissions**
   ```bash
   chmod 755 ~/votre_projet
   chmod 777 ~/autogpt/uploads
   ```

## Vérification et débogage

1. **Vérification des logs**
   - Aller dans l'onglet "Web"
   - Consulter les sections :
     - Error log
     - Server log
     - Access log

2. **Points de vérification**
   - [ ] Tous les fichiers sont présents dans la bonne structure
   - [ ] Les permissions sont correctement configurées
   - [ ] Les variables d'environnement sont définies
   - [ ] Les dépendances sont installées
   - [ ] Le dossier 'uploads' est accessible en écriture

## Utilisation

1. **Interface utilisateur**
   - Accéder à `votre-username.pythonanywhere.com`
   - Utiliser la zone de glisser-déposer pour les fichiers
   - Utiliser le chat pour interagir avec AutoGPT

2. **Limites et restrictions**
   - Taille maximale des fichiers : 16 MB
   - Types de fichiers autorisés : txt, pdf, png, jpg, jpeg, gif, doc, docx
   - Durée maximale de stockage des fichiers : selon votre plan PythonAnywhere

## Dépannage

1. **Problèmes courants**
   - Erreur 500 : Vérifier les logs pour plus de détails
   - Erreur 403 : Vérifier les permissions des dossiers
   - Erreur d'upload : Vérifier les limites de taille et les permissions

2. **Solutions**
   - Redémarrer l'application web
   - Vérifier les logs d'erreur
   - Confirmer que tous les packages sont installés
   - Vérifier les variables d'environnement

## Support

Pour toute question ou problème :
1. Consulter les logs PythonAnywhere
2. Vérifier la documentation Flask
3. Contacter le support PythonAnywhere si nécessaire

## Notes de sécurité

- Ne jamais exposer vos clés API
- Toujours valider les fichiers uploadés
- Limiter l'accès aux dossiers sensibles
- Mettre à jour régulièrement les dépendances
