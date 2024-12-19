import os
import ast
import time
import psutil
import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Configuration du logging avec rotation des fichiers
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('optimizer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class CodeModification:
    old: str
    new: str
    description: str
    priority: int = 0

class CodeOptimizer:
    def __init__(self):
        self.dynamic_functions: Dict[str, str] = {}
        self.MAX_DYNAMIC_FUNCTIONS = 100
        self.memory_threshold = 0.9  # 90% de la mémoire disponible
        self.temp_dir = Path(tempfile.gettempdir()) / "code_optimizer"
        self.temp_dir.mkdir(exist_ok=True)
        self.setup_nlp()

    def setup_nlp(self):
        """Initialisation du modèle NLP avec un modèle plus stable"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            self.model = AutoModelForCausalLM.from_pretrained("gpt2", device_map='auto')
            self.nlp = pipeline("text-generation", 
                              model=self.model, 
                              tokenizer=self.tokenizer,
                              device_map='auto')
            logger.info("Modèle NLP initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur d'initialisation du modèle NLP: {e}")
            self.nlp = None

    def check_memory(self) -> bool:
        """Vérification de l'utilisation mémoire"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent < (self.memory_threshold * 100)
        except Exception as e:
            logger.error(f"Erreur lors de la vérification mémoire: {e}")
            return False

    def generate_file(self, filename: str, content: str) -> bool:
        """Génère un fichier avec gestion des erreurs améliorée"""
        if not self.check_memory():
            logger.error("Mémoire insuffisante pour générer le fichier")
            return False

        try:
            safe_path = self.temp_dir / Path(filename).name
            with open(safe_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Fichier '{safe_path}' généré avec succès")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la génération du fichier: {e}")
            return False

    def optimize_code(self, code: str) -> Tuple[str, float]:
        """Optimisation de code avec analyses statiques avancées et métriques"""
        start_time = time.time()
        try:
            if not self.check_memory():
                return code, 0.0

            tree = ast.parse(code)
            
            class AdvancedOptimizer(ast.NodeTransformer):
                def visit_Name(self, node):
                    optimizations = {
                        'i': 'index',
                        'x': 'value',
                        'l': 'list_data',
                        'dict': 'dictionary',
                        'str': 'string',
                        'tmp': 'temporary',
                        'arr': 'array',
                        'lst': 'list',
                        'num': 'number',
                        'func': 'function',
                        'var': 'variable'
                    }
                    if node.id in optimizations:
                        return ast.copy_location(
                            ast.Name(id=optimizations[node.id], ctx=node.ctx),
                            node
                        )
                    return node

                def visit_For(self, node):
                    self.generic_visit(node)
                    return node

            optimized_tree = AdvancedOptimizer().visit(tree)
            optimized_code = ast.unparse(optimized_tree)
            
            # Validation du code optimisé
            ast.parse(optimized_code)
            
            optimization_time = time.time() - start_time
            return optimized_code, optimization_time
        except Exception as e:
            logger.error(f"Erreur lors de l'optimisation du code: {e}")
            return code, 0.0

    def add_dynamic_function(self, name: str, func_code: str) -> bool:
        """Ajout sécurisé de fonction dynamique avec validation"""
        if not self.check_memory():
            logger.error("Mémoire insuffisante pour ajouter une fonction")
            return False

        try:
            if len(self.dynamic_functions) >= self.MAX_DYNAMIC_FUNCTIONS:
                oldest_func = min(self.dynamic_functions.items(), key=lambda x: x[1])
                del self.dynamic_functions[oldest_func[0]]
                logger.info(f"Fonction '{oldest_func[0]}' supprimée pour libérer de l'espace")
            
            if name in self.dynamic_functions:
                raise ValueError(f"La fonction '{name}' existe déjà")

            # Validation du code
            ast.parse(func_code)
            
            # Environnement isolé
            namespace = {}
            exec(func_code, namespace)
            
            if name not in namespace:
                raise ValueError(f"La fonction '{name}' n'a pas été définie")

            self.dynamic_functions[name] = func_code
            globals()[name] = namespace[name]
            
            logger.info(f"Fonction '{name}' ajoutée dynamiquement")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout de la fonction: {e}")
            return False

    def modify_source_code(self, filename: str, modifications: List[CodeModification]) -> bool:
        """Modification sécurisée du code source avec backup"""
        if not self.check_memory():
            return False

        backup_file = self.temp_dir / f"{Path(filename).name}.backup"
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Le fichier {filename} n'existe pas")

            with open(filename, 'r', encoding='utf-8') as source:
                code = source.read()
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(code)

            modifications.sort(key=lambda x: x.priority, reverse=True)
            for mod in modifications:
                code = code.replace(mod.old, mod.new)
                logger.info(f"Modification appliquée: {mod.description}")

            ast.parse(code)

            with open(filename, 'w', encoding='utf-8') as file:
                file.write(code)

            logger.info(f"Fichier source '{filename}' modifié avec succès")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de la modification: {e}")
            if os.path.exists(backup_file):
                os.replace(str(backup_file), filename)
                logger.info("Restauration de la sauvegarde effectuée")
            return False

    def process_natural_language_command(self, command: str) -> Optional[str]:
        """Traitement des commandes en langage naturel avec validation"""
        if self.nlp is None or not self.check_memory():
            return None

        try:
            prompt = f"Generate Python function for: {command}\n\ndef"
            result = self.nlp(prompt, 
                            max_length=200, 
                            num_return_sequences=1,
                            temperature=0.7)[0]['generated_text']
            
            code = f"def{result.split('def', 1)[1]}"
            ast.parse(code)
            
            return code
        except Exception as e:
            logger.error(f"Erreur lors du traitement NLP: {e}")
            return None

    def cleanup(self):
        """Nettoyage des ressources"""
        try:
            self.nlp = None
            self.model = None
            self.tokenizer = None
            import gc
            gc.collect()
            logger.info("Nettoyage effectué")
        except Exception as e:
            logger.error(f"Erreur nettoyage: {e}")

def main():
    optimizer = CodeOptimizer()
    
    try:
        # Test d'optimisation
        code_example = """
def calculate_sum(l):
    x = 0
    for i in l:
        x += i
    return x
    """
        optimized_code, optimization_time = optimizer.optimize_code(code_example)
        logger.info(f"Code optimisé en {optimization_time:.2f} secondes:\n{optimized_code}")

        # Test de fonction dynamique
        dynamic_function = """
def analyze_data(data_list):
    return sum(data_list) / len(data_list) if data_list else 0
    """
        optimizer.add_dynamic_function('analyze_data', dynamic_function)

        # Test de modification
        modifications = [
            CodeModification(
                old="calculate_sum",
                new="sum_values",
                description="Renommage fonction",
                priority=1
            )
        ]
        
        try:
            while True:
                if optimizer.check_memory():
                    optimizer.modify_source_code('script.py', modifications)
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Arrêt demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
    finally:
        optimizer.cleanup()

if __name__ == "__main__":
    main()