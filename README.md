# MacroX AI Validator — Plataforma de Validación Nutricional Inteligente

MacroX es una aplicación web moderna  que automatiza la validación y el filtrado inteligente de registros alimenticios utilizando Inteligencia Artificial local. El sistema asegura que las entradas de texto correspondan estrictamente a contenidos de nutrición y dieta antes de ser procesados por los módulos de conteo calórico.

---

## 🏗️ 1. Arquitectura del Código Fuente y Configuración

El proyecto está estructurado bajo el framework robusto **Django 5.0.6**, siguiendo un patrón modular:

* **`config/`**: Núcleo de configuración del proyecto.
    * `settings.py`: Contiene el registro maestro de la aplicación (`api.apps.ApiConfig`) y las variables globales del entorno.
    * `urls.py`: Enrutador principal que redirige las peticiones HTTP hacia los módulos correspondientes.
* **`api/`**: Módulo central de la Inteligencia Artificial y la lógica de negocio.
    * `apps.py`: Implementa la estrategia de **Carga Perezosa (*Lazy Loading*)**. Levanta el modelo en la memoria RAM una sola vez al arrancar el servidor mediante el método `ready()`, evitando cuellos de botella.
    * `views.py`: Procesa las solicitudes de validación mediante una política multiclase y aplica la regla de negocio del piso seguro ($60\%$).
    * `urls.py`: Define el endpoint seguro `/validator/`.
* **`templates/ & static/`**: Interfaz de usuario Premium construida con Bootstrap 5 y comunicación asíncrona mediante **JavaScript (Fetch API)** para evitar recargas de pantalla.

---

## 🐳 2. Infraestructura y Contenedores (Dockerfile)

Para garantizar la portabilidad y el despliegue idéntico en entornos PaaS (como Railway), el proyecto cuenta con una receta de empaquetado optimizada:

* **`Dockerfile`**: Basado en `python:3.11-slim` para reducir el tamaño del contenedor. Instala dependencias del sistema mínimas y transfiere el código base expuesto en el puerto `8000`.
* **`requirements.txt`**: Configurado específicamente con la bandera `--find-links` para forzar la instalación de **PyTorch en su versión ligera para CPU (`torch==2.3.1+cpu`)**, reduciendo la huella de almacenamiento de gigabytes a solo unos cuantos megabytes.

---

## 📡 3. Integración de la API y Flujo de Comunicación

La API funciona bajo un flujo estrictamente asíncrono y protegido por el token CSRF de Django:

1.  **Entrada:** El usuario envía un texto plano desde el Front a través de una petición HTTP `POST` hacia `/validator/`.
2.  **Inferencia:** La vista invoca el pipeline local de Hugging Face (`transformers.pipeline`) cargado en memoria, evaluando el texto sobre una matriz de etiquetas candidatas.
3.  **Salida:** La API responde en devolviendo un objeto estructurado en formato **JSON**:

![Ilustración 1. Validación de texto de usuario](/evidencias/valido2.jpg)

Objeto JSON leido a través de una respuesta asíncrona de AJAX (JavaScript), cuyo formato se da en la ilustración anterior.

```json
{
    "is_food": true,
    "detected_category": "Comida y nutricion",
    "confidence": 0.7258,
    "message": "Contenido Válido. Se detectó contenido de Comida y Nutrición con un 72.58% de certeza."
}
```

Por otro lado, cuando el modelo "Validator" detecta que el contenido (texto de usuario) no esta relacionado con Comida y Nutrición, despliega el siguiente mensasaje:

![Ilustración 2. Validación de texto de usuario](/evidencias/novalido.jpg)

Objeto JSON leido a través de una respuesta asíncrona de AJAX (JavaScript), cuyo formato se da en la ilustración anterior.

```json
{
    "is_food": False,
    "detected_category": "Actividades",
    "confidence": 0.4762,
    "message": "El contenido principal detectado fue 'Actividades' (47.62%), pero se espera un contenido sobre Comida y Nutrición."
}
```

## 📝 4. Casos de Prueba Evaluados en el Backend

Durante esta fase de desarrollo, se sometió al validador de IA a una batería de pruebas con frases cotidianas y complejas para medir el comportamiento del umbral de confianza (50%):

1. **Frase de Éxito Típica:** * *Texto:* "Hoy almorcé pechuga de pollo con arroz integral y aguacate."
   * *Comportamiento esperado:* Aceptado de forma directa.

2. **Frase con Vocabulario Mezclado (Falso Positivo Potencial):**
   * *Texto:* "Ayer fui al gimnasio a entrenar pierna y luego compré unos tenis nuevos."
   * *Comportamiento esperado:* Rechazado, ya que el enfoque es deportivo/moda y no nutricional.

3. **Frase de Contexto Ambiguo (Caso Frontera):**
   * *Texto:* "La manzana de la discordia causó problemas en la reunión de la oficina."
   * *Comportamiento esperado:* Rechazado, al detectar el uso metafórico de la palabra "manzana".

4. **Entrada de Texto Vacía:**
   * *Texto:* ""
   * *Comportamiento esperado:* Interceptado por la lógica de validación previa a la inferencia (HTTP 400).
  
## 5. Resultados y Conclusiones de la Fase Actual

* **Validación Temprana y Aislamiento:** El objetivo principal de esta fase se ha cumplido con éxito. El sistema logra **discriminar y validar exclusivamente el texto de entrada**, garantizando que el usuario esté registrando información alineada a la nutrición antes de interactuar con la persistencia de datos. Esto optimiza el uso de cómputo y blinda la base de datos de registros basura o irrelevantes.

* **Evolución del Sistema (Fase Futura):** Es importante destacar que el alcance de la fase actual se limita estrictamente al filtrado y clasificación del texto (saber si es comida o no). En una fase posterior del proyecto, una vez aprobado el acceso del texto, se integrará un módulo de **Reconocimiento de Entidades Nombradas (NER)**. Este segundo componente será el encargado de desmenuzar la frase internamente para extraer los alimentos específicos y sus cantidades exactas (ej. "pechuga de pollo" -> 200g) para su posterior cálculo calórico automatizado.
