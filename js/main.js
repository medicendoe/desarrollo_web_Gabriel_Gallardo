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

// Función para agregar más campos de fotos
function agregarCampoFoto() {
    const container = document.getElementById('photo-inputs-container');
    const nuevoInput = document.createElement('input');
    nuevoInput.type = 'file';
    nuevoInput.name = 'fotos[]';
    nuevoInput.accept = 'image/*';
    container.appendChild(nuevoInput);
}

// Función que se ejecuta cuando el DOM está completamente cargado
document.addEventListener('DOMContentLoaded', async function() {
    // Cargar las regiones al cargar la página
    await cargarRegiones();
    
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
});