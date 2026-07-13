<script>
document.getElementById('validator-form').addEventListener('submit', async function(e) {
    e.preventDefault(); // Evita que la página se recargue

    const form = e.target;
    const formData = new FormData(form);
    const textInput = document.getElementById('text_input');
    const submitBtn = form.querySelector('button[type="submit"]');
    const submitIcon = submitBtn.querySelector('.material-icons');
    
    const container = document.getElementById('result-container');
    const alertBox = document.getElementById('result-alert');
    const resIcon = document.getElementById('result-icon');
    const resTitle = document.getElementById('result-title');
    const resText = document.getElementById('result-text');

    // 1. Estado de Carga (Feedback visual en el botón)
    submitBtn.disabled = true;
    submitIcon.innerText = 'sync'; // Cambia el icono de enviar por uno de carga
    submitIcon.classList.add('spin-animation'); // Efecto de rotación

    try {
        // 2. Llamada asíncrona a tu URL de Django
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();

        // 3. Procesar la respuesta del JSON de MacroX
        container.classList.remove('d-none'); // Mostramos el contenedor
        
        if (data.is_food) {
            // Estilo Éxito: Fondo verde oscuro mate con texto claro
            alertBox.className = "alert alert-success d-flex align-items-center justify-content-start rounded-4 border-0 p-3 shadow-sm text-start bg-success bg-opacity-10 text-success";
            resIcon.innerText = 'check_circle';
            resTitle.innerText = `Validación Exitosa (${(data.confidence * 100).toFixed(1)}%)`;
            resText.innerText = data.message;
        } else {
            // Estilo Rechazo: Fondo rojo oscuro mate con texto claro
            alertBox.className = "alert alert-danger d-flex align-items-center justify-content-start rounded-4 border-0 p-3 shadow-sm text-start bg-danger bg-opacity-10 text-danger";
            resIcon.innerText = 'error';
            resTitle.innerText = `Contenido No Válido (${(data.confidence * 100).toFixed(1)}%)`;
            resText.innerText = data.message;
        }

    } catch (error) {
        // Manejo de errores de conexión o del servidor
        container.classList.remove('d-none');
        alertBox.className = "alert alert-warning d-flex align-items-center justify-content-start rounded-4 border-0 p-3 shadow-sm text-start bg-warning bg-opacity-10 text-warning";
        resIcon.innerText = 'warning';
        resTitle.innerText = 'Error de comunicación';
        resText.innerText = 'No se pudo conectar con el servidor de Macrox AI.';
    } finally {
        // 4. Restaurar el botón a su estado original
        submitBtn.disabled = false;
        submitIcon.innerText = 'send';
        submitIcon.classList.remove('spin-animation');
    }
});
</script>