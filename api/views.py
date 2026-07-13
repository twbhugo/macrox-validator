from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .apps import ApiConfig

def home_view(request):
    return render(request, 'index.html')

@csrf_protect
def validator_view(request):

    print("Accediendo a la vista Validator...")
    #Validar que la petición sea estrictamente un POST enviado por el formulario
    if request.method == 'POST':
        texto_usuario = request.POST.get('text_input', '').strip()
        print(f"\nMétodo: {request.method}\nTexto capturado: {texto_usuario}\nContinuando con la validación...")
        
        #Validar el texto no este vacio
        if not texto_usuario:
            return JsonResponse({"error:" : "El texto no puede estar vacío"}, status=400)
        
        #Verificar que el clasificador esté operativo en la RAM
        if ApiConfig.classifier is None:
            return JsonResponse({
                "is_food": False,
                "detected_category": "Error del Sistema",
                "confidence": 0.0,
                "message": "El modelo de Inteligencia Artificial se está inicializando. Reintenta en unos segundos."
            }, status=503)

        #Ejecutar la inferencia real de Hugging Face
        resultado = ApiConfig.classifier(
            texto_usuario, 
            candidate_labels=ApiConfig.etiquetas_candidatas
        )
        print("Validación completa.")

        #Extraer la categoría ganadora absoluta (índice 0 gracias al auto-sort del pipeline)
        etiqueta_ganadora = resultado['labels'][0]
        score_ganador = resultado['scores'][0]

        #Comparar la lógica de negocio multiclase y piso seguro (60%)
        es_comida_valida = False
        mensaje_usuario = ""
            
        if etiqueta_ganadora == "Comida y Nutrición":
            if score_ganador >= ApiConfig.piso_seguro:
                es_comida_valida = True
                mensaje_usuario = f" Se detectó contenido de Comida y Nutrición con un {score_ganador * 100:.2f}% de certeza."
            else:
                mensaje_usuario = f"Se detectó un intento de texto sobre Comida y Nutrición, pero la certeza ({score_ganador * 100:.2f}%) es menor al piso seguro requerido del {ApiConfig.piso_seguro * 100}%."
        else:
            mensaje_usuario = f"El contenido principal detectado fue '{etiqueta_ganadora}' ({score_ganador * 100:.2f}%), pero se espera un contenido sobre Comida y Nutrición."
        
        response_data = {
                "is_food": es_comida_valida,
                "detected_category": etiqueta_ganadora,
                "confidence": round(score_ganador, 4),
                "message": mensaje_usuario
            }
        return JsonResponse(response_data)
    
    #Si la peticion es GET,devolver un error de petición inválida
    return JsonResponse({"error": "Acceso no permitido"}, status=400)