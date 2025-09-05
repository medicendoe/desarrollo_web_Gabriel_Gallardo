// Función para cargar dinámicamente un script
function cargarScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`No se pudo cargar el script: ${src}`));
        document.head.appendChild(script);
    });
}

// Función para cargar las regiones en el select
async function cargarRegiones() {
    // Verificar si region_comuna ya está disponible, si no, cargar el script
    if (typeof region_comuna === 'undefined') {
        try {
            await cargarScript('./js/region_comuna.js');
        } catch (error) {
            console.error('Error cargando region_comuna.js:', error);
            return;
        }
    }
    
    const selectRegion = document.getElementById('region');
    
    // Limpiar opciones existentes (mantener la primera opción)
    selectRegion.innerHTML = '<option value="">Seleccione una región</option>';
    
    // Agregar todas las regiones del archivo region_comuna.js
    region_comuna.regiones.forEach(region => {
        const option = document.createElement('option');
        option.value = region.numero;
        option.textContent = region.nombre;
        selectRegion.appendChild(option);
    });
}

// Función para cargar las comunas según la región seleccionada
function cargarComunas(regionSeleccionada) {
    const selectComuna = document.getElementById('comuna');
    
    // Limpiar opciones existentes
    selectComuna.innerHTML = '<option value="">Seleccione una comuna</option>';
    
    if (regionSeleccionada) {
        // Buscar la región seleccionada
        const region = region_comuna.regiones.find(r => r.numero == regionSeleccionada);
        
        if (region) {
            // Agregar todas las comunas de la región seleccionada
            region.comunas.forEach(comuna => {
                const option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                selectComuna.appendChild(option);
            });
        }
    }
}

// Función para manejar el cambio de región
function manejarCambioRegion() {
    const selectRegion = document.getElementById('region');
    const regionSeleccionada = selectRegion.value;
    cargarComunas(regionSeleccionada);
}

// Función para mostrar/ocultar el campo de URL de contacto según la red social seleccionada
function manejarCambioRedSocial() {
    const selectRedSocial = document.getElementById('red-social');
    const contactUrlGroup = document.getElementById('contact-url-group');
    
    if (selectRedSocial.value && selectRedSocial.value !== '') {
        contactUrlGroup.style.display = 'block';
    } else {
        contactUrlGroup.style.display = 'none';
    }
}

// Función para agregar más campos de fotos (máximo 5)
function agregarCampoFoto() {
    const container = document.getElementById('photo-inputs-container');
    const inputs = container.querySelectorAll('input[type="file"]');
    
    if (inputs.length < 5) {
        const nuevoInput = document.createElement('input');
        nuevoInput.type = 'file';
        nuevoInput.name = 'fotos[]';
        nuevoInput.accept = 'image/*';
        container.appendChild(nuevoInput);
        
        // Si ya hay 5 campos, deshabilitar el botón
        if (inputs.length + 1 >= 5) {
            document.getElementById('add-photo-btn').disabled = true;
            document.getElementById('add-photo-btn').textContent = 'Máximo 5 fotos permitidas';
        }
    }
}

// Función para pre-llenar la fecha de entrega (fecha actual + 3 horas)
function preLlenarFechaEntrega() {
    const fechaEntregaInput = document.getElementById('fecha-entrega');
    const fechaActual = new Date();
    fechaActual.setHours(fechaActual.getHours() + 3);
    
    // Formatear la fecha al formato datetime-local (YYYY-MM-DDTHH:mm)
    const year = fechaActual.getFullYear();
    const month = String(fechaActual.getMonth() + 1).padStart(2, '0');
    const day = String(fechaActual.getDate()).padStart(2, '0');
    const hours = String(fechaActual.getHours()).padStart(2, '0');
    const minutes = String(fechaActual.getMinutes()).padStart(2, '0');
    
    const fechaFormateada = `${year}-${month}-${day}T${hours}:${minutes}`;
    fechaEntregaInput.value = fechaFormateada;
    
    // Guardar la fecha mínima para validación posterior
    fechaEntregaInput.dataset.fechaMinima = fechaFormateada;
}

// Función que se ejecuta cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', async function() {
    // Cargar las regiones al cargar la página
    await cargarRegiones();
    
    // Pre-llenar la fecha de entrega con fecha actual + 3 horas
    preLlenarFechaEntrega();
    
    // Agregar event listener para el cambio de región
    const selectRegion = document.getElementById('region');
    if (selectRegion) {
        selectRegion.addEventListener('change', manejarCambioRegion);
    }
    
    // Agregar event listener para el cambio de red social
    const selectRedSocial = document.getElementById('red-social');
    if (selectRedSocial) {
        selectRedSocial.addEventListener('change', manejarCambioRedSocial);
    }
    
    // Agregar event listener para el botón de agregar foto
    const addPhotoBtn = document.getElementById('add-photo-btn');
    if (addPhotoBtn) {
        addPhotoBtn.addEventListener('click', agregarCampoFoto);
    }
    
    // Agregar event listener para el envío del formulario
    const formulario = document.getElementById('adoption-form');
    if (formulario) {
        formulario.addEventListener('submit', manejarEnvioFormulario);
    }
});

// Función para validar el formato de email
function validarEmail(email) {
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    return regex.test(email);
}

// Función para validar el formato del número de celular
function validarCelular(celular) {
    const regex = /^\+\d{3}\.\d{8}$/;
    return regex.test(celular);
}

// Función para validar todos los campos del formulario
function validarFormulario() {
    const errores = [];
    
    // ========== SECCIÓN 1: ¿DÓNDE? ==========
    const region = document.getElementById('region').value;
    if (!region || region === '') {
        errores.push('Debe seleccionar una región');
    }
    
    const comuna = document.getElementById('comuna').value;
    if (!comuna || comuna === '') {
        errores.push('Debe seleccionar una comuna');
    }
    
    const sector = document.getElementById('sector').value;
    if (sector && sector.length > 100) {
        errores.push('El sector no debe superar los 100 caracteres');
    }
    
    // ========== SECCIÓN 2: ¿CONTACTO? ==========
    const nombre = document.getElementById('nombre').value.trim();
    if (!nombre || nombre.length < 3 || nombre.length > 200) {
        errores.push('El nombre debe tener entre 3 y 200 caracteres');
    }
    
    const email = document.getElementById('email').value.trim();
    if (!email || email.length > 100 || !validarEmail(email)) {
        errores.push('Debe ingresar un email válido (máximo 100 caracteres)');
    }
    
    const celular = document.getElementById('celular').value.trim();
    if (celular && !validarCelular(celular)) {
        errores.push('El número de celular debe tener el formato +NNN.NNNNNNNN');
    }
    
    const redSocial = document.getElementById('red-social').value;
    const contactUrl = document.getElementById('contact-url').value.trim();
    if (redSocial && redSocial !== '') {
        if (!contactUrl || contactUrl.length < 4 || contactUrl.length > 50) {
            errores.push('El ID o URL de contacto debe tener entre 4 y 50 caracteres cuando se selecciona una red social');
        }
    }
    
    // ========== SECCIÓN 3: ¿QUÉ MASCOTA? ==========
    const tipoMascota = document.getElementById('tipo-mascota').value;
    if (!tipoMascota || tipoMascota === '') {
        errores.push('Debe seleccionar el tipo de mascota');
    }
    
    const cantidad = parseInt(document.getElementById('cantidad').value);
    if (!cantidad || cantidad < 1) {
        errores.push('La cantidad debe ser un número entero mayor o igual a 1');
    }
    
    const edad = parseInt(document.getElementById('edad').value);
    if (!edad || edad < 1) {
        errores.push('La edad debe ser un número entero mayor o igual a 1');
    }
    
    const unidadEdad = document.getElementById('unidad-edad').value;
    if (!unidadEdad || unidadEdad === '') {
        errores.push('Debe seleccionar la unidad de medida de la edad');
    }
    
    const fechaEntrega = document.getElementById('fecha-entrega').value;
    const fechaMinima = document.getElementById('fecha-entrega').dataset.fechaMinima;
    if (!fechaEntrega) {
        errores.push('Debe seleccionar una fecha de entrega');
    } else if (fechaEntrega < fechaMinima) {
        errores.push('La fecha de entrega debe ser mayor o igual a la fecha pre-llenada');
    }
    
    // Validar fotos (mínimo 1, máximo 5)
    const inputsFoto = document.querySelectorAll('input[type="file"][name="fotos[]"]');
    let fotosSeleccionadas = 0;
    inputsFoto.forEach(input => {
        if (input.files && input.files.length > 0) {
            fotosSeleccionadas++;
        }
    });
    
    if (fotosSeleccionadas < 1) {
        errores.push('Debe subir al menos 1 foto');
    } else if (fotosSeleccionadas > 5) {
        errores.push('No puede subir más de 5 fotos');
    }
    
    return errores;
}

// Función para mostrar mensajes de error
function mostrarErrores(errores) {
    // Eliminar mensajes de error anteriores
    const erroresAnteriores = document.querySelectorAll('.mensaje-error');
    erroresAnteriores.forEach(error => error.remove());
    
    if (errores.length > 0) {
        const formulario = document.getElementById('adoption-form');
        const divErrores = document.createElement('div');
        divErrores.className = 'mensaje-error';
        divErrores.style.cssText = 'background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 15px; margin: 20px 0; border-radius: 4px;';
        
        let htmlErrores = '<h3>Por favor corrija los siguientes errores:</h3><ul>';
        errores.forEach(error => {
            htmlErrores += `<li>${error}</li>`;
        });
        htmlErrores += '</ul>';
        
        divErrores.innerHTML = htmlErrores;
        formulario.insertBefore(divErrores, formulario.firstChild);
        
        // Hacer scroll al principio del formulario para mostrar los errores
        formulario.scrollIntoView({ behavior: 'smooth' });
    }
}

// Función para mostrar el mensaje de éxito
function mostrarMensajeExito() {
    const body = document.body;
    body.innerHTML = `
        <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
            <h1 style="color: #4caf50;">¡Éxito!</h1>
            <p style="font-size: 18px; margin: 30px 0;">Hemos recibido la información de adopción, muchas gracias y suerte!</p>
            <button onclick="window.location.href='index.html'" 
                    style="background: #2196F3; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">
                Volver a la Portada
            </button>
        </div>
    `;
}

// Función principal para manejar el envío del formulario
function manejarEnvioFormulario(event) {
    // Prevenir el envío por defecto
    event.preventDefault();
    
    // Ejecutar todas las validaciones
    const errores = validarFormulario();
    
    if (errores.length > 0) {
        // Si hay errores, mostrarlos y detener el proceso
        mostrarErrores(errores);
        return;
    }
    
    // Si no hay errores, mostrar confirmación
    const confirmacion = confirm('¿Está seguro que desea agregar este aviso de adopción?');
    
    if (confirmacion) {
        // Usuario presionó "Aceptar"
        mostrarMensajeExito();
    }
    // Si presionó "Cancelar", no hacer nada (mantener al usuario en el formulario)
}