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
        """
        Este método se ejecuta AUTOMÁTICAMENTE una sola vez cuando Django arranca.
        Aquí cargamos el modelo desde los archivos locales.
        """
        # Evitamos ejecuciones dobles que Django hace por el auto-reload en desarrollo
        print("Accediendo al modelo...")
        if os.environ.get('RUN_MAIN') == 'true' or not settings.DEBUG:
            ruta_modelo = os.path.join(settings.BASE_DIR, 'model_weights')
            print("🧠 MACROX AI: Cargando clasificador Zero-Shot en memoria RAM...")
            print(f"📂 Ruta origen: {ruta_modelo}")
            
            try:
                # Cargamos el pipeline usando los pesos locales descargados de Colab
                ApiConfig.classifier = pipeline(
                    task="zero-shot-classification",
                    model=ruta_modelo,
                    tokenizer=ruta_modelo
                )
                print("🟢 MACROX AI: ¡Modelo cargado exitosamente y listo para validar!")
            
            except Exception as e:
                print("🔴 MACROX AI: Error crítico al cargar los pesos del modelo local.")
                print(f"❌ Detalle: {str(e)}")