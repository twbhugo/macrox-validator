    

import os
from django.apps import AppConfig
from django.conf import settings
from transformers import pipeline

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    #Variables globales de la app que sostendrán el modelo en memoria
    print("Declarando hiperparametros...")
    classifier = None
    etiquetas_candidatas = ["Comida y Nutrición", "Otros temas"]
    piso_seguro = 0.50

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true' or os.environ.get('SERVER_SOFTWARE', '').startswith('gunicorn'):
            ruta_modelo = os.path.join(settings.BASE_DIR, 'model_weights')
            
            if os.path.exists(ruta_modelo) and os.path.exists(os.path.join(ruta_modelo, 'config.json')):
                print("🟢 MACROX AI: Cargando modelo DeBERTa-v3 local...")
                model_path = ruta_modelo
                tokenizer_path = ruta_modelo
            else:
                print("☁️ MACROX AI: Carpeta vacía. Descargando DeBERTa-v3 desde Hugging Face...")
                model_path = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
                tokenizer_path = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

            try:
                ApiConfig.classifier = pipeline(
                    task="zero-shot-classification",
                    model=model_path,
                    tokenizer=tokenizer_path
                )
                print("🚀 MACROX AI: ¡DeBERTa-v3 cargado exitosamente en RAM!")
            except Exception as e:
                print(f"❌ MACROX AI: Error al cargar el modelo: {str(e)}")